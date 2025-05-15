from crewai import Agent, Crew, Task
from logging_config import get_logger
from crewai_tools import FileReadTool

class ResearchCrew:
    def __init__(self, verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.crew = self.create_crew()
        self.logger.info("ResearchCrew initialized")

    def create_crew(self):
        self.logger.info("Creating research crew with agents")
        
        fileReader = Agent(
            role='File Reader',
            goal='Read the input text from a CSV file and return a list of all URLS, their X handle and other contact (if any), in a pure format without any additional notes or shortening',
            backstory='Expert at extracting and identifying key information in its entirety',
            verbose=self.verbose
        )

        self.logger.info("Created research and writer agents")

        crew = Crew(
            agents=[fileReader],
            tasks=[
                Task(
                    description='Analyse: {text} and return A consise list of all URLS, with their corrosponding X handles and contacts beside them for each company' ,
                    expected_output="""A consise list of all URLS, with their corrosponding X handles and contacts beside them
                                        for each company, the output MUST adhere to the following output structure:

                                        Company: COMPANY_NAME 
                                            - Url: URL
                                            - X-handle: X HANDLE
                                            - Other contact: OTHER CONTACT
                                                                
                                        The following guidelines are of utmost importance:
                                            -Under NO CIRCUMSTANCES should the analysis be cut short for brevity.
                                            -The whole output must be returned no matter how long it is.
                                            - The output must be a pure list, no additional notes are to be added.
                                            - There should be the SAME amount of elements as there are companies,
                                                as each element is for each company.
                                                absolutely ZERO parts of the input text can be ignored. 
                                                All lines MUST be read and an appropriate output for each company.
                                            - If ANY of these fields cannot be identified, it should be returned as "unable to find FIELD"
                                            -The URLS would lead to a website when searched, so anomalous text should not be mistaken for a URL
                                        If any of said guidelines are not followed, the task is considered failed
                                        and the output completely invalid.


                                        """,
                    agent=fileReader,
                )
            ]
        )
        self.logger.info("Crew setup completed")
        return crew