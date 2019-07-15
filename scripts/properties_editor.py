distributionUrl = "distributionUrl=https\://services.gradle.org/distributions/gradle-5.5-all.zip\n"

"""
Edit the gradle.properties file to ensure version 5 is being used

For now, script is given a relative file handle when its main method is called.
"""

def edit_properties(file_handle):
    # open the file
    file_r = open(file_handle, "r")

    # get the lines
    lines = file_r.readlines()

    new_lines = []

    # iterate through the lines, find the line beginning "distributionUrl="
    for line in lines:
        if line[0:16] == "distributionUrl=":
            new_lines.append(distributionUrl)
        else:
            new_lines.append(line)

    file_r.close()

    # write the new lines to the file
    file_w = open(file_handle, "w")

    [file_w.write(line) for line in new_lines]

    file_w.close()

    print("done properties edit.")
