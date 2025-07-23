import traceback
import sims4.commands

import services
from drama_scheduler.dialog_drama_node import DialogDramaNode
from game_services import service_manager
from event_testing.resolver import SingleSimResolver

# Create an instance of the mod when the script is loaded
_command_type = sims4.commands.CommandType.Live
_PREFIX = "dt"
logger = sims4.log.Logger("drama_dialog", default_owner="ParametricPolymorphism")


def generic_command(command_name):
    def command(function):
        @sims4.commands.Command(command_name, command_type=_command_type)
        def wrapper(*args, _connection=None):
            output = sims4.commands.CheatOutput(_connection)
            # noinspection PyBroadException
            try:
                function(*args, _connection)
            except Exception as ex:
                tb = traceback.format_exc()
                output(tb)
                logger.exception("Failed to execute command")

    return command


def trigger_dialog_drama_node(sim_info, drama_node_id):
    """
    Triggers a dialog drama node for the specified sim

    :param sim_info: The SimInfo of the sim to target
    :param drama_node_id: The ID of the dialog drama node to trigger
    """
    # Get drama node manager
    drama_node_manager = services.get_instance_manager(sims4.resources.Types.DRAMA_NODE)

    if drama_node_manager is None:
        logger.error("Could not find drama node manager")
        return False

    # Get the drama node class by ID
    drama_node_tuning = drama_node_manager.get(drama_node_id)

    if drama_node_tuning is None:
        logger.error(f"Could not find drama node with ID {drama_node_id}")
        return False

    if not issubclass(drama_node_tuning, DialogDramaNode):
        logger.error(f"Drama node with ID {drama_node_id} is not a DialogDramaNode")
        return False

    # Create an instance of the drama node
    drama_node_instance = drama_node_tuning(sim_info=sim_info)
    logger.info(f"Created drama node instance")

    # Check if the drama node can run
    if hasattr(drama_node_instance, 'validate_for_sim'):
        result = drama_node_instance.validate_for_sim(sim_info)
        if not result:
            logger.error(f"ERROR: Drama node validation failed: {result}")
            return False
        logger.info("Drama node validation passed")

    # Try setup first
    if hasattr(drama_node_instance, 'setup'):
        resolver = SingleSimResolver(sim_info)
        # Create an instance of the drama node
        drama_node_instance = drama_node_tuning(sim_info=sim_info)
        # Set up the drama node with the resolver
        logger.info("Calling setup()")
        drama_node_instance.setup(resolver=resolver)

    # Run the drama node
    logger.info("Calling _run()")
    result = drama_node_instance._run()
    logger.info(f"Run result: {result}")
    return result


# Command to manually trigger backup
@generic_command(f"{_PREFIX}.trigger_dialog_drama_node")
def trigger_dialog_drama_node_command(drama_node_id=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    # Get client and active sim
    client = services.client_manager().get_first_client()
    if client is None:
        output("No client found")
        return False

    # Get the active sim (currently selected sim)
    active_sim = client.active_sim
    if active_sim is None:
        output("No active sim found")
        return False

    # Get sim_info of the active sim
    sim_info = active_sim.sim_info
    drama_node_id = int(drama_node_id)
    output(f"Triggering dialog drama node with ID {drama_node_id}")
    result = trigger_dialog_drama_node(sim_info=sim_info, drama_node_id=drama_node_id)
    if result:
        output("Successfully triggered dialog drama node")
    else:
        output("Failed to trigger dialog drama node")


