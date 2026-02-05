import pandas as pd
import sys

# data.py
# --------------------------------------------------------------
# ALL FUNCTIONS TO BE PROGRAMMATICALLY TESTED ARE IN THIS FILE.
# --------------------------------------------------------------
# This file serves as the backend data layer for the application, implemented using the MissionData class.
# Implementation and usage of this class is demonstrated in main.py.

class MissionData:
    def __init__(self, fileName: str):
        try:
            self.csv = pd.read_csv(fileName)

            # Check if CSV is empty
            if self.csv.empty:
                raise ValueError("CSV file is empty.")

            self.csv["Date"] = pd.to_datetime(self.csv["Date"], format="%Y-%m-%d")

            self.minYear = self.csv["Date"].dt.year.min()
            self.maxYear = self.csv["Date"].dt.year.max()

            self.totalCompanies = self.csv["Company"].nunique()
        except:
            print("Either the filename is incorrect, the CSV is empty, or the file is not a proper CSV format.")
            print("Please try again with a valid CSV file.")
            sys.exit(1)

    # Function 1
    def getMissionCountByCompany(self, companyName: str) -> int:
        try:
            return self.csv["Company"].value_counts()[companyName]
        except:
            print("Company not found. Input is case-sensitive.")
            return 0
    
    # Function 2
    def getSuccessRate(self, companyName: str) -> float:
        try:
            companyData = self.csv[self.csv["Company"] == companyName]
            companySuccesses = companyData[companyData["MissionStatus"] == "Success"]
            percentSuccess = (len(companySuccesses) / len(companyData)) * 100

            return round(percentSuccess, 2)
        except:
            print("Company not found. Input is case-sensitive.")
            return 0.0
    
    # Function 3
    def getMissionsByDateRange(self, startDate: str, endDate: str) -> list:
        try:
            # Error will raise if date format is incorrect
            start = pd.to_datetime(startDate, format="%Y-%m-%d", errors="raise")
            end = pd.to_datetime(endDate, format="%Y-%m-%d", errors="raise")

            # Additional date validation
            if (start > end):
                raise ValueError("Start date must be before end date.")
            
            if start > pd.Timestamp.now() or end > pd.Timestamp.now():
                raise ValueError("Dates cannot be in the future.")
        
            missionsInRange = self.csv[(self.csv["Date"] >= start) & (self.csv["Date"] <= end)]
            missionsInRange = missionsInRange.sort_values("Date")

            return missionsInRange["Mission"].tolist()
        except:
            print("Either the date formats are invalid or the date range is invalid.")
            return []

    # Function 4
    def getTopCompaniesByMissionCount(self, n: int) -> list:
        try:
            # Input validation
            if n <= 0:
                raise ValueError("Input must be a positive integer.")
            
            # In case that n is larger than total number of companies, adjust n to total number of companies and keep expected behavior.
            if n > self.totalCompanies:
                n = self.totalCompanies

            companyCounts = self.csv["Company"].value_counts()
            sortedCompanyList = sorted(companyCounts.items(), key=lambda x: (-x[1], x[0])) # Sort by count descending, name ascending

            return sortedCompanyList[:n]
        except:
            print("Either input was not a valid positive integer or an error occurred while processing the data.")
            return []
        
    # Function 5
    def getMissionStatusCount(self) -> dict:
        try:
            statusCounts = self.csv["MissionStatus"].value_counts().to_dict()
            
            return statusCounts
        except:
            print("An error occurred while processing the data.")
            return {}
        
    # Function 6
    def getMissionsByYear(self, year: int) -> int:
        try:
            # Input validation, I did it based on year range in data set
            if (year < self.minYear) or (year > self.maxYear):
                raise ValueError("Year is out of range of data set.")

            missionCount = len(self.csv[self.csv["Date"].dt.year == year])

            return missionCount
        except:
            print("Either year is invalid or out of range of data set. Minimum year: {}, Maximum year: {}".format(self.minYear, self.maxYear))
            return 0
    
    # Function 7
    def getMostUsedRocket(self) -> str:
        try:
            missionsPerRocket = self.csv["Rocket"].value_counts()
            maxMissions = missionsPerRocket.max()

            topRockets = missionsPerRocket[missionsPerRocket == maxMissions]

            return sorted(topRockets.index)[0]
        except:
            print("An error occurred while processing the data.")
            return ""
    
    # Function 8
    def getAverageMissionsPerYear(self, startYear: int, endYear: int) -> float:
        try:
            # Input validation
            if startYear > endYear:
                raise ValueError("Start year must be less than or equal to end year.")
            
            if startYear < self.minYear or endYear > self.maxYear:
                raise ValueError("Year range is out of bounds of data set.")

            totalYears = endYear - startYear + 1

            missionCount = len(self.csv[(self.csv["Date"].dt.year >= startYear) & (self.csv["Date"].dt.year <= endYear)])

            averageMissions = missionCount / totalYears

            return round(averageMissions, 2)
        except:
            print("Years are invalid or out of bounds of data set. Minimum year: {}, Maximum year: {}".format(self.minYear, self.maxYear))
            return 0.0