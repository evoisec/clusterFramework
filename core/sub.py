import sys, time
import csv
import json
import subprocess
from google.cloud import pubsub_v1

# this is just a skeleton/placeholder for a Workflow State Machine (if needed) - for the moment the role of such
# will be played by the CO Audit Log
class WorkflowStateMachine:

    def __init__(self, is_first_cycle, event_map, event_queue):
        self.is_first_cycle = is_first_cycle
        self.event_map = event_map
        self.event_queue = event_queue


# Enforces strictly sequential message processing (in combination with the used synchronous pull pubsub client type)
NUM_MESSAGES = 1
# the default ACK time for the topic
MESSAGE_ACK_TIME = 10

EVENT_MAP_FILE_NAME = 'event-map.csv'

def main():

    project_id = "studied-client-297916"
    cc_topic_subscription_id = "cc-internal"

    cc_topic_subscriber = pubsub_v1.SubscriberClient()
    cc_topic_subscription_path = cc_topic_subscriber.subscription_path(project_id, cc_topic_subscription_id)


    event_map = {}
    with open(EVENT_MAP_FILE_NAME, newline='') as csvfile:
        event_map_reader = csv.reader(csvfile, skipinitialspace=True, delimiter=',')
        for event_map_row in event_map_reader:
            print(event_map_row)

            key = event_map_row[0]
            del event_map_row[0]
            print(event_map_row)
            event_map[key] = event_map_row

    #print(event_map.get("ledger_refresh_completion"))
    #print(event_map.get("ledger_refresh_completion")[0])
    #sys.exit(0)

    workflow_state_machine = WorkflowStateMachine(True, event_map, [])


    ##############################################################################################
    # This is the main Central Orchestrator (CO) processing loop. It cycles through each topic (currently only one), processes the messages/events and
    # updates the CO Audit Log and Workflow State Machine. It exits if it receives a command from the command topic
    ##############################################################################################
    while True:

        print("################### Start of New Event Message Processing Cycle #########################################################")

        workflow_state_machine = process_cc_int_topic(cc_topic_subscriber, cc_topic_subscription_path, workflow_state_machine)


############################################################################################################
# Note, while processing the messages/events in a topic, here we can loop until all messages are processed
# still one message at a time ie Strictly Sequentially or we can process just one message per each invocation
# of this function
# The current implementation processes strictly one event message per invocation
############################################################################################################
def process_cc_int_topic(subscriber, subscription_path, workflow_state_machine):


    # this is synchrnous pull pubsub client - its use is part of the solution for Strictly Sequential Event Processing

    received_message = pull_sync_message(subscriber, subscription_path)

    if received_message != None and workflow_state_machine.is_first_cycle == True:

        # ToDO: On first connection to the topic, Ignore and ACK all Event Messages with timestamp older than the
        # the system time when the connection to the topic was establsihed

        ############################################################################
        # Go to the end of the topic and start consuming messages from there. Execute this step only once, on first connection to the topic,
        # Ignore and ACK all Event Messages with timestamp older than the the system time when the new/first connection to
        # the topic was establsihed
        ############################################################################

        # ToDO: add system time comparison with message timestamp to position precisely at a message which was received after CO launched

        print("Just launched for the first time, positioning at the end of the message topic/queue, thus skpipping all old message in the topic/queue")
        workflow_state_machine.is_first_cycle = False

        while received_message != None:
            ack_message(subscriber, subscription_path, received_message)
            received_message = pull_sync_message(subscriber, subscription_path)

        return workflow_state_machine

    if received_message == None and workflow_state_machine.is_first_cycle == True:

        workflow_state_machine.is_first_cycle = False

        return workflow_state_machine

    if received_message == None and workflow_state_machine.is_first_cycle == False:

        return workflow_state_machine

######################################################################################################################
#
# Retrieve all pending messages from the topic and persist them in the CO Audit Log which playes a role as a classic Queue
#
######################################################################################################################

    # this is a temp hack required onlty for testing
    last_received_message = None

    while received_message != None:

        last_received_message = received_message

        #ToDO: Dedup the Event Message

        ############################################################################
        # Dedup the Event Message against CO Audit Log, here also skip any further processing - if dedup conditions encountered
        ############################################################################

        # ACK immediately if duplicate or already processed and go back to the message consumption step

        print("Deduping the Event Message against the CO Audit Log")

        #ToDO: Persist the Event Message to the CO Audit Log

        ############################################################################
        # Persist the Event Message in CO Audit Log conditional on only if it doesnt already exist there
        # When done here, it prevents Race Conditions between CO and the CC Workflows when updating the CO Audit Log
        # This step corresponds to Workflow State = Event Message Received by CO and Stored in CO Audit Log
        ############################################################################

        print("Persisting the Event Message to the CO Audit Log")

        ############################################################################
        # Acknowledge the Event Message to GCP PUBSUB
        ############################################################################

        # simulates business processing so the time for ACK expires - to be removed, used only for testing/simulation
        # default topic time for ACK is 10 sec
        #time.sleep(MESSAGE_ACK_TIME + 10)

        # will not throw error is the ACK time for the message has expired - so here we are just making best effort to ACK
        # the dedup step which will be invoked during the next itteration, will ensure/double check that the message is ACKed

        ack_message(subscriber, subscription_path, received_message)

        received_message = pull_sync_message(subscriber, subscription_path)


####################################################################################################################################################
#
# End of the First Phase of the CO Event Processing Cycle and Start of the Second Phase
#
# First Phase: Persist all CURRENTLY pending / available message from the topic to the CO Audit Log
#
# Second Phase: Process all outstanding messages in the CO Audit Log by launching CC Argo Workflows
#
####################################################################################################################################################


    #ToDO: Perform business processing for the messages in the current topic and then update / process the Workflow State MAchine based on the received events/messages

    # For Each Pending Message in CO Audit Log perform the following steps:

    ############################################################################
    # Map Event Message to CC Argo Workflow Name
    ############################################################################

    print("Mapping Event Message to CC Argo Workflow Name")

    # last_received_message is a temp hack only for testing this branch of the program - replace with event data retrieved from CO Audit Log

    event_data = last_received_message.message.data
    event_data_json = json.loads(event_data)

    event_name = event_data_json["event_name"]
    print(event_name)

    workflow_names = workflow_state_machine.event_map.get(event_name)

    for workflow_name in workflow_names:

        print(workflow_name)
        reporting_date  = event_data_json["reporting_date"]
        print(reporting_date)

        cmd_str = workflow_name + " " + event_data.decode("utf-8") + " " + reporting_date

        ############################################################################
        # Trigger CC Argo Workflow by invoking the "argo submit" as a shell command
        ############################################################################
        print("Triggering CC Argo Workflow")

        # the echo command will be replaced with argo submit - this ia version only for when using the eacho command which
        # part of / embedded in the OS schell
        process = subprocess.Popen(['echo', cmd_str], stdout=subprocess.PIPE, universal_newlines=True, shell=True)
        # uncomment this when using the actual argo submit command
        # process = subprocess.Popen(['echo', workflow_name], stdout=subprocess.PIPE, universal_newlines=True)

        # note, the below approach keeps receiving as a real-time stream, the output form the launched command and this provides it with
        # opportunity to parse it an dmake decisions about error conditions etc in real-time
        while True:
            output = process.stdout.readline()
            print(output.strip())
            # Do something else
            return_code = process.poll()
            if return_code is not None:
                print('RETURN CODE', return_code)
                # Process has finished, read rest of the output
                for output in process.stdout.readlines():
                    print(output.strip())
                break

        ############################################################################
        # Keep checking (for awhile) the CO Audit Log whether the CC Workflow had started - loop for a configurable interval
        # if necessary raise alert
        # this can be enhanced further by streaming the real-time log of the CC Argo Workflow with the "argo submit --log" command
        # and parsing and scanning the log for error conditions
        ############################################################################
        print("Checking whether the CC Argo Workflow has started")


        # ToDO: perform final operations on the State Machine if necessary, before return

    return workflow_state_machine


def pull_sync_message(subscriber, subscription_path):

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": NUM_MESSAGES},
        #retry=retry.Retry(deadline=300),
    )

    if len(response.received_messages) != 0:

        received_message = response.received_messages[0]
        print(received_message)

        print(f"GCP PUBSUB Message ID: {received_message.message.message_id}.")
        print(f"Received: {received_message.message.data}.")

        if received_message.message.attributes:
            print("Attributes:")
            for key in received_message.message.attributes:
                value = received_message.message.attributes.get(key)
                print(f"{key}: {value}")

        return received_message

    else:

        return None

def ack_message(subscriber, subscription_path, received_message):
    ack_ids = [received_message.ack_id]
    request = {"subscription": subscription_path, "ack_ids": ack_ids}
    subscriber.acknowledge(request)

    print(f"Received, logged in CO Audit Table and made best effort to acknowledge one message from {subscription_path}.")

if __name__ == "__main__":
    main()