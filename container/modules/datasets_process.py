from rdetoolkit.exceptions import catch_exception_with_message
from rdetoolkit.models.rde2types import RdeInputDirPaths, RdeOutputResourcePath
from rdetoolkit.rde2util import Meta

from modules.graph_handler import GraphPlotter
from modules.inputfile_handler import FileReader
from modules.meta_handler import MetaParser, get_invoice_obj
from modules.structured_handler import StructuredDataProcessor


class CustomProcessingCoordinator:
    """Coordinator class for managing custom processing modules.

    This class serves as a coordinator for custom processing modules, facilitating the use of
    various components such as file reading, metadata parsing, graph plotting, and structured
    data processing. It is responsible for managing these components and providing an organized
    way to execute the required tasks.

    Args:
        file_reader (FileReader): An instance of the file reader component.
        meta_parser (MetaParser): An instance of the metadata parsing component.
        graph_plotter (GraphPlotter): An instance of the graph plotting component.
        structured_processer (StructuredDataProcessor): An instance of the structured data
                                                        processing component.

    Attributes:
        file_reader (FileReader): The file reader component for reading input data.
        meta_parser (MetaParser): The metadata parsing component for processing metadata.
        graph_plotter (GraphPlotter): The graph plotting component for visualization.
        structured_processer (StructuredDataProcessor): The component for processing structured data.

    Example:
        custom_module = CustomProcessingCoordinator(FileReader(), MetaParser(), GraphPlotter(), StructuredDataProcessor())
        # Note: The method 'execute_processing' hasn't been defined in the provided code,
        #       so its usage is just an example here.
        custom_module.execute_processing(srcpaths, resource_paths)

    """

    def __init__(self, file_reader: FileReader, meta_parser: MetaParser, graph_plotter: GraphPlotter, structured_processer: StructuredDataProcessor) -> None:
        """Initialize the coordinator with the specified components."""
        self.file_reader = file_reader
        self.meta_parser = meta_parser
        self.graph_plotter = graph_plotter
        self.structured_processer = structured_processer


def scatterplot_module(srcpaths: RdeInputDirPaths, resource_paths: RdeOutputResourcePath) -> None:
    """Process input data to generate scatterplot visualizations and save structured data.

    Args:
        srcpaths (RdeInputDirPaths): Paths to the source directories containing input files.
        resource_paths (RdeOutputResourcePath): Paths to the output directories for saving processed files.

    This function performs the following steps:
    1. Initializes the processing module with custom components for reading files, parsing metadata, plotting graphs, and processing structured data.
    2. Retrieves user-defined graph options from the invoice JSON file.
    3. Reads the input data file and extracts metadata and data.
    4. Saves the data to CSV files, including a subset of columns specified by the user.
    5. Saves the header information to a text file.
    6. Parses and saves metadata based on a metadata definition JSON file.
    7. Generates and saves a scatterplot image based on the input data and user-defined options.

    """
    module = CustomProcessingCoordinator(FileReader(), MetaParser(), GraphPlotter(), StructuredDataProcessor())

    # -- user setting --
    invoice_json = get_invoice_obj(srcpaths.invoice.joinpath("invoice.json"))
    invoice_json.to_json(srcpaths.invoice.joinpath("invoice.json"))
    user_graph_options = module.graph_plotter.create_options(invoice_json)
    user_setting_header = [user_graph_options.xlabel, user_graph_options.ylabel] if user_graph_options.xlabel and user_graph_options.ylabel else None
    basename = resource_paths.rawfiles[0].stem

    # -- Read Input File --
    module.file_reader.set_mesurement_start_number(resource_paths.rawfiles[0], resource_paths.invoice_org)
    meta, df_data = module.file_reader.read(resource_paths.rawfiles[0])

    # -- Save structured data (1 header csv) --
    module.structured_processer.to_csv(df_data, resource_paths.struct.joinpath("data.csv"))
    module.structured_processer.to_csv(
        df_data.iloc[:, [user_graph_options.x_col_num, user_graph_options.y_col_num]],
        resource_paths.struct.joinpath(f"{basename}.csv"),
        header=user_setting_header,
    )
    # -- Save header information --
    module.structured_processer.to_text(meta, resource_paths.struct.joinpath("header.csv"))

    # -- Save meta data --
    module.meta_parser.parse(meta, srcpaths.tasksupport.joinpath("metadata-def.json"))
    module.meta_parser.save_meta(resource_paths.meta.joinpath("metadata.json"), Meta(srcpaths.tasksupport.joinpath("metadata-def.json")))

    # -- Plot a graph and Save Figure --
    module.graph_plotter.plot(
        df_data,
        resource_paths.main_image.joinpath(resource_paths.rawfiles[0].stem),
        user_graph_options,
    )


@catch_exception_with_message(error_message="ERROR: failed in data processing", error_code=50, verbose=True)
def dataset(srcpaths: RdeInputDirPaths, resource_paths: RdeOutputResourcePath) -> None:
    """Wrap structured processing.

    Args:
        srcpaths (RdeInputDirPaths): Paths to input resources for processing.
        resource_paths (RdeOutputResourcePath): Paths to output resources for saving results.

    Returns:
        None

    """
    # ---------------------
    # Define user-specific processing:
    # for example, file naming conventions, data preprocessing, data analysis functions, etc.
    # ---------------------
    scatterplot_module(srcpaths, resource_paths)
