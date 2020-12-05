import csv
import matplotlib.pyplot as plt
import datetime


class CsvReader:
    """
    Static class to read a csv file taken from NI Air website and plot the csv_data on a graph
    """

    @staticmethod
    def csv_reader(file_path):
        """
        Static method to read data from a csv file
        :param file_path: The complete file path of the csv file
        :return: The data read from the csv file
        """
        csv_data = []
        reader = csv.reader(open(file_path), delimiter=",")
        y = 0
        for row in reader:
            x = 0
            if y != 0:
                data_row = []
                for element in row:
                    if x in [0, 1, 3, 5]:  # Only read from the 1st, 2nd, 4th, and 6th columns
                        if element == "nodata":  # If statement to store a no data reading as None
                            element = None
                        if y != 1:
                            if x == 0:
                                # Store the date in a dd/mm/yyyy format
                                element = datetime.datetime.strptime(element, '%d/%m/%Y')
                            elif element is not None:
                                element = int(element)  # Convert the concentrations to integers
                        data_row.append(element)
                    x += 1
                csv_data.append(data_row)
            y += 1
        return csv_data

    @staticmethod
    def plotter(csv_data, graph_name):
        """
        Static method to plot the graphs with ozone, NO2 and SO2 concentrations over time
        :param csv_data: The data from the csv file
        :param graph_name: The file name that the graph should be saved as
        """
        dates = []
        ozones_sample = []
        ozones = []
        no2_sample = []
        no2 = []
        so2_sample = []
        so2 = []

        for i in range(1, len(csv_data)):  # Ignore the 1st line as these are table headers
            ozones_sample.append(csv_data[i][1])
            no2_sample.append(csv_data[i][2])
            so2_sample.append(csv_data[i][3])

            # Sample every 30 days, changing the modulus will change the time period sampled
            if i % 30 == 0 or i == len(csv_data):
                ozones_avg = CsvReader.calculate_avg(ozones_sample)
                no2_avg = CsvReader.calculate_avg(no2_sample)
                so2_avg = CsvReader.calculate_avg(so2_sample)

                ozones_sample = []
                no2_sample = []
                so2_sample = []

                dates.append(csv_data[i][0])
                ozones.append(ozones_avg)
                no2.append(no2_avg)
                so2.append(so2_avg)

        plt.plot(dates, ozones, label=csv_data[0][1])
        plt.plot(dates, no2, label=csv_data[0][2])
        plt.plot(dates, so2, label=csv_data[0][3])
        plt.grid()
        plt.xlabel('Dates')
        plt.ylabel('Concentration (V µg/m³)')
        plt.legend()
        plt.savefig(graph_name)
        plt.show()

    @staticmethod
    def calculate_avg(sample):
        """
        Static helper method to calculate the average of the readings over a set time period to aid plotting the graphs
        :param sample: The sample of readings to be averaged
        :return: The average of the sample readings
        """
        sum = 0
        count = 0
        avg = None
        for reading in sample:
            if reading is not None:
                sum += reading
                count += 1
        if count != 0:
            avg = sum / count
        return avg


if __name__ == '__main__':
    # Type in the complete file paths of the csv files in quotes
    # Use .\\ for a relative path to the main.py
    file_paths = [".\\example_csv_1.csv",
                  ".\\example_csv_2.csv"]
    # Type in the desired file names for the graphs in quotes, including the file format such as .svg or .eps
    graph_names = ["example_graph_1.svg",
                   "example_graph_2.svg"]

    if len(file_paths) == len(graph_names):  # Validation check to ensure the each csv file has a name for its graph
        j = 0
        for each in file_paths:
            data = CsvReader.csv_reader(each)
            CsvReader.plotter(data, graph_names[j])
            j += 1
    else:
        print("You do not have the same number of graph names as csv files to read!")
