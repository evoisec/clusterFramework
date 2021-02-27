import sys, time
from google.cloud import pubsub_v1

# this is just a skeleton/placeholder for a Workflow State Machine (if needed) - for the moment the role of such
# will be played by the CO Audit Log
class WorkflowStateMachine:

    def __init__(self, message_id, is_first_cycle):
        self.gcp_message_id = message_id
        self.is_first_cycle = is_first_cycle


# Enforces strictly sequential message processing (in combination with the used synchronous pull pubsub client type)
NUM_MESSAGES = 1
# the default ACK time for the topic
MESSAGE_ACK_TIME = 10

def main():

    project_id = "studied-client-297916"
    cc_topic_subscription_id = "cc-internal"

    cc_topic_subscriber = pubsub_v1.SubscriberClient()
    cc_topic_subscription_path = cc_topic_subscriber.subscription_path(project_id, cc_topic_subscription_id)

    gcp_message_id = None

    workflow_state_machine = WorkflowStateMachine(None, True)


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
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": NUM_MESSAGES},
        #retry=retry.Retry(deadline=300),
    )

    if len(response.received_messages) != 0:

        # ToDO: On first connection to the topic, Ignore and ACK all Event Messages with timestamp older than the
        # the system time when the connection to the topic was establsihed

        ############################################################################
        # Go to the end of the topic and start consuming messages from there. Execute only once, On first connection to the topic,
        # Ignore and ACK all Event Messages with timestamp older than the the system time when the new/first connection to
        # the topic was establsihed
        ############################################################################

        if workflow_state_machine.is_first_cycle:

            print("Just launched for the first time, positioning at the end of the message topic/queue, thus skpipping all old message in the topic/queue")
            workflow_state_machine.is_first_cycle = False


        received_message = response.received_messages[0]
        print(received_message)
        print(f"Received: {received_message.message.data}.")
        ack_ids = [received_message.ack_id]

        if received_message.message.attributes:
                print("Attributes:")
                for key in received_message.message.attributes:
                    value = received_message.message.attributes.get(key)
                    print(f"{key}: {value}")


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
        request = {"subscription": subscription_path, "ack_ids": ack_ids}
        subscriber.acknowledge(request)

        print( f"Received, logged in CO Audit Table and made best effort to acknowledge {len(response.received_messages)} messages from {subscription_path}." )

        #ToDO: Perform business processing for the messages in the current topic and then update / process the Workflow State MAchine based on the received events/messages


        ############################################################################
        # Map Event Message to CC Argo Workflow Name
        ############################################################################

        print("Mapping Event Message to CC Argo Workflow Name")

        ############################################################################
        # Trigger CC Argo Workflow by invoking the "argo submit" as a shell command
        ############################################################################
        print("Triggering CC Argo Workflow")

        ############################################################################
        # Keep checking (for awhile) the CO Audit Log whether the CC Workflow had started - loop for a configurable interval
        # if necessary raise alert
        # this can be enhanced further by streaming the real-time log of the CC Argo Workflow with the "argo submit --log" command
        # and parsing and scanning the log for error conditions
        ############################################################################
        print("Checking whether the CC Argo Workflow has started")


    # ToDO: perform final operation on the State Machine before return



    return workflow_state_machine



if __name__ == "__main__":
    main()