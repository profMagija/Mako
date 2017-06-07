
from ..schedule import * 
from ..reporting import * 
from ..ams.actions import * 
from ..ams import * 

class MakoDatabase(object):

    def uploadProjects(self, projects):
        pass

    def uploadMeasurementActions(self, actions):
        pass

    def uploadMeasurementData(self, action_id, data):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        pass

    def uploadData(self, data):
        """
        Data is list of tuples where first element is name and second concrete data 
        """
        pass

    def uploadSchedules(self, schedules):
        """
        schedules: list of tuples where:

        1. element: date of creation (or None if db does not provide it)
        2. element: list of all projects 
        3. element: list of schedule entries
        """
        pass

    def uploadReports(self, reports):
        pass


    def downloadProjects(self):
        pass

    def downloadMeasurementActions(self):
        pass

    def downloadMeasurementData(self, action_id):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        pass

    def downloadData(self):
        """
        Returns list of tuples where first element is name and second is data 
        """
        pass

    def downloadSchedules(self):
        """
        Returns list of Schedule object
        """
        pass

    def downloadReports(self):
        pass

    def toDict(self):
        d = {}
        d["projects"] = [] 
        projects = self.downloadProjects()
        for project in projects:
            d["projects"].append(project.toDict())
        
        d["schedules"] = []
        schedules = self.downloadSchedules()
        for schedule in schedules:
            d["schedules"].append(schedule.toDict())

        metrics = self.downloadMeasurementActions()
        d["metrics"] = [] 
        d["data"] = []
        for metric in metrics:
            d["metrics"].append(metric.toDict())
            data = self.downloadMeasurementData(metric.getIdentifier())
            dd = {"id": metric.getIdentifier()}
            dd["data"] = [] 
            for val in data:
                dd["data"].append({"date": datetime.datetime.strftime(val[0], "%Y-%m-%d"), "value": val[1]})
            d["data"].append(dd)
        d["reports"] = [] 
        reports = self.downloadReports()
        for report in reports:
            d["reports"].append(report.toDict())
        return d

    def fromDict(self, d):
        projects = []
        for project in d["projects"]:
            projects.append(ScheduleProject.fromDict(project))
        self.uploadProjects(projects)
        
        schedules = []
        for schedule in d["schedules"]:
            schedules.append(Schedule.fromDict(schedule))
        self.uploadSchedules(schedules)
        
        ams = AMS()
        metrics = []
        for metric in d["metrics"]:
            metrics.append(ams.getAction(metric))
        self.uploadMeasurementActions(metrics)

        reports = []
        for report in d["reports"]:
            reports.append(Report.fromDict(report))
        self.uploadReports(reports)

        for data_obj in d["data"]:
            data = []
            for val in data_obj["data"]:
                data.append((datetime.datetime.strptime(val["date"], "%Y-%m-%d"), float(val["value"])))
            self.uploadMeasurementData(data_obj["id"], data)
