import os

"""
This script is to modify the maven pom.xml file to include errorprone
"""

def modify_pom(pom_path):
    file = open(pom_path, "r")
    lines = file.readlines()

    # search for the plugins line
    found = False
    index = 0

    # first remove whitespace from the start of all lines
    # check they are not empty
    if len(lines) == 0:
        lines = ['']

    index = 0
    for line in lines:
        lines[index] = clean_line(line)
        index += 1

    index = 0
    for line in lines:
        if line[0:9] == "<plugins>":
            lines[index] = line + \
                           "\n<plugin>\n  " + \
                                    "<groupId>org.apache.maven.plugins</groupId>\n" + \
                                    "<artifactId>maven-compiler-plugin</artifactId>\n" + \
                                    "<version>3.8.0</version>\n" + \
                                    "<configuration>\n" + \
                                        "<source>8</source>\n" + \
                                        "<target>8</target>\n" + \
                                        "<compilerArgs>\n" + \
                                            "<arg>-XDcompilePolicy=simple</arg>\n" + \
                                            "<arg>-Xplugin:ErrorProne</arg>" + \
                                        "</compilerArgs>\n" + \
                                        "<annotationProcessorPaths>\n" + \
                                            "<path>" + \
                                                "<groupId>com.google.errorprone</groupId>" + \
                                                "<artifactId>error_prone_core</artifactId>" + \
                                                "<version>2.3.4-SNAPSHOT</version>" + \
                                            "</path>\n" + \
                                        "</annotationProcessorPaths>\n" + \
                                    "</configuration>\n" + \
                                "</plugin>\n"

        index += 1

    # now remove the file and replace it with the new one
    os.remove(pom_path)

    new_build_file = open(pom_path, "w")
    new_build_file.writelines(lines)

    print("done modifying build.gradle for: " + pom_path)

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


modify_pom("testpom.xml")