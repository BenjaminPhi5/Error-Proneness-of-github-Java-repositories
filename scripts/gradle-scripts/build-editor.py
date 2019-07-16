import os

"""
This script is intended to modify the build file (for gradle projects)
to switch the compiler to using error prone.

sample build script:
plugins {
    id 'java'
    id "net.ltgt.errorprone" version "0.8.1"
}

group 'test'
version '1.0-SNAPSHOT'

sourceCompatibility = 1.8

repositories {
    mavenCentral()
}

dependencies {
    errorprone "com.google.errorprone:error_prone_core:2.3.3"
}

"""

"""
NOTE: if the repositories tag is there and the others aren't its putting dependencies before repositories... hope
this isn't too bad.
"""

lines = []


"""make sure to give an expanded filepath that the os module can use to remove the file"""
def modify_build(file_handle):
    # file handle is  of form */build.gradle
    build_file = open(file_handle, "r")

    # get the lines
    lines = build_file.readlines()

    # check they are not empty
    if len(lines) == 0:
        lines = ['']

    index = 0
    for line in lines:
        lines[index] = clean_line(line)
        index += 1

    plugins = False
    dependencies = False

    index = 0

    for line in lines:
        if line[0:7] == "plugins":
            lines[index] = "plugins {\nid \"net.ltgt.errorprone\" version \"0.8.1\"\n"
            plugins = True

        elif line[0:12] == "dependencies":
            lines[index] = "dependencies {\nerrorprone \"com.google.errorprone:error_prone_core:2.3.3\"\n"
            dependencies = True

        index += 1

    print("aftcheck:\n",lines)
    print(dependencies)
    print(plugins)

    if not dependencies:
        if not plugins:
            # put in the dependencies line at the top
            lines[0] = "dependencies {\nerrorprone \"com.google.errorprone:error_prone_core:2.3.3\"\n}\n" + lines[0]
        else:
            # if plugins are there, need to put it below the plugins
            brace = 0
            insert_now = False
            index = 0
            for line in lines:
                if line[0:7] == "plugins":
                    brace = 1
                elif brace == 1 and line[0] == "}":
                    # put dependencies after the line:
                    insert_now = True
                if insert_now:
                    lines[index] = "dependencies {\nerrorprone \"com.google.errorprone:error_prone_core:2.3.3\"\n}\n" + line

                index += 1

    print("dep:\n", lines)

    if not plugins:
        # now put the plugins in
        lines[0] = "plugins {\nid \"net.ltgt.errorprone\" version \"0.8.1\"\n}\n" + lines[0]


    # make sure lines are all separate now
    lines = split_on_newline(lines)

    # now deal with repositories
    start_line = ""
    start_index = 0
    found = False
    print("len start: ", len(start_line))
    index = 0

    for line in lines:
        if line[0:12] == "repositories":
            start_line = line
            start_index = index
        elif line[0:14] == "mavenCentral()":
            if start_line != "":
                found = True

        index += 1

    print("start_line: |", start_line, "|")
    print("len start: ", len(start_line))
    print("found: ", found)

    if len(start_line) != 0:
        if found == False:
            # repositories tag exists and the mavenCentral is missing
            lines[start_index] = start_line + "mavenCentral()\n"

    else:
        # repositories tabs missing, add them before dependencies
        print("add repositories called")
        index = 0;
        for line in lines:
            print("line: |", line, " | line[0:12]: ", line[0:12])
            if line[0:12] == "dependencies":
                lines[index] = "repositories {\nmavenCentral()\n}\n" + line

            index += 1


    # now remove the file and replace it with the new one
    os.remove(file_handle)

    new_build_file = open(file_handle, "w")
    new_build_file.writelines(lines)

    print("done modifying build.gradle for: " + file_handle)


# split all the newline chars into actual separate lines
def split_on_newline(lines):
    new_lines = []
    for line in lines:
        new_line = ""
        count = 0
        start = 0
        for c in line:
            if c == "\n":
                new_lines.append(line[start:count] + "\n")
                new_line = ""
                # plus 1 to exclude the \n
                start = count + 1
            count += 1
        if len(new_line) != 0:
            new_lines.append(new_line)

    # copy in new lines
    return new_lines


def clean_line(line):
    # if line is empty return
    if len(line) == 0:
        return line

    # remove any spaces at the start of the line
    if line[0] != ' ':
        return line
    else:
        count = 0
        for c in line:
            if c == ' ':
                count += 1
            else:
                break

        line = line[count:]
        return line

# need to delete the empty space infront of each line to ensure that this works


# do dependencies,
# then repositories
# then plugins above it

