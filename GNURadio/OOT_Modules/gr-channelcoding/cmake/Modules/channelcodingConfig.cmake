INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_CHANNELCODING channelcoding)

FIND_PATH(
    CHANNELCODING_INCLUDE_DIRS
    NAMES channelcoding/api.h
    HINTS $ENV{CHANNELCODING_DIR}/include
        ${PC_CHANNELCODING_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    CHANNELCODING_LIBRARIES
    NAMES gnuradio-channelcoding
    HINTS $ENV{CHANNELCODING_DIR}/lib
        ${PC_CHANNELCODING_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(CHANNELCODING DEFAULT_MSG CHANNELCODING_LIBRARIES CHANNELCODING_INCLUDE_DIRS)
MARK_AS_ADVANCED(CHANNELCODING_LIBRARIES CHANNELCODING_INCLUDE_DIRS)

