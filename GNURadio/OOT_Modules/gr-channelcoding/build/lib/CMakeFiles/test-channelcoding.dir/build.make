# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build

# Include any dependencies generated for this target.
include lib/CMakeFiles/test-channelcoding.dir/depend.make

# Include the progress variables for this target.
include lib/CMakeFiles/test-channelcoding.dir/progress.make

# Include the compile flags for this target's objects.
include lib/CMakeFiles/test-channelcoding.dir/flags.make

lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o: lib/CMakeFiles/test-channelcoding.dir/flags.make
lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o: ../lib/test_channelcoding.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o"
	cd /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/lib && /usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o -c /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/lib/test_channelcoding.cc

lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.i"
	cd /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/lib && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/lib/test_channelcoding.cc > CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.i

lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.s"
	cd /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/lib && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/lib/test_channelcoding.cc -o CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.s

lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o.requires:

.PHONY : lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o.requires

lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o.provides: lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o.requires
	$(MAKE) -f lib/CMakeFiles/test-channelcoding.dir/build.make lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o.provides.build
.PHONY : lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o.provides

lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o.provides.build: lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o


lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o: lib/CMakeFiles/test-channelcoding.dir/flags.make
lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o: ../lib/qa_channelcoding.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o"
	cd /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/lib && /usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o -c /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/lib/qa_channelcoding.cc

lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.i"
	cd /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/lib && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/lib/qa_channelcoding.cc > CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.i

lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.s"
	cd /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/lib && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/lib/qa_channelcoding.cc -o CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.s

lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o.requires:

.PHONY : lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o.requires

lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o.provides: lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o.requires
	$(MAKE) -f lib/CMakeFiles/test-channelcoding.dir/build.make lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o.provides.build
.PHONY : lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o.provides

lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o.provides.build: lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o


# Object files for target test-channelcoding
test__channelcoding_OBJECTS = \
"CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o" \
"CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o"

# External object files for target test-channelcoding
test__channelcoding_EXTERNAL_OBJECTS =

lib/test-channelcoding: lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o
lib/test-channelcoding: lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o
lib/test-channelcoding: lib/CMakeFiles/test-channelcoding.dir/build.make
lib/test-channelcoding: /usr/local/lib/libgnuradio-runtime.so
lib/test-channelcoding: /usr/local/lib/libgnuradio-pmt.so
lib/test-channelcoding: /usr/lib/x86_64-linux-gnu/libboost_filesystem.so
lib/test-channelcoding: /usr/lib/x86_64-linux-gnu/libboost_system.so
lib/test-channelcoding: /usr/lib/x86_64-linux-gnu/libcppunit.so
lib/test-channelcoding: lib/libgnuradio-channelcoding.so
lib/test-channelcoding: /usr/local/lib/libgnuradio-runtime.so
lib/test-channelcoding: /usr/local/lib/libgnuradio-pmt.so
lib/test-channelcoding: /usr/lib/x86_64-linux-gnu/libboost_filesystem.so
lib/test-channelcoding: /usr/lib/x86_64-linux-gnu/libboost_system.so
lib/test-channelcoding: lib/CMakeFiles/test-channelcoding.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX executable test-channelcoding"
	cd /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/lib && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test-channelcoding.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
lib/CMakeFiles/test-channelcoding.dir/build: lib/test-channelcoding

.PHONY : lib/CMakeFiles/test-channelcoding.dir/build

lib/CMakeFiles/test-channelcoding.dir/requires: lib/CMakeFiles/test-channelcoding.dir/test_channelcoding.cc.o.requires
lib/CMakeFiles/test-channelcoding.dir/requires: lib/CMakeFiles/test-channelcoding.dir/qa_channelcoding.cc.o.requires

.PHONY : lib/CMakeFiles/test-channelcoding.dir/requires

lib/CMakeFiles/test-channelcoding.dir/clean:
	cd /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/lib && $(CMAKE_COMMAND) -P CMakeFiles/test-channelcoding.dir/cmake_clean.cmake
.PHONY : lib/CMakeFiles/test-channelcoding.dir/clean

lib/CMakeFiles/test-channelcoding.dir/depend:
	cd /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/lib /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/lib /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/lib/CMakeFiles/test-channelcoding.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : lib/CMakeFiles/test-channelcoding.dir/depend

