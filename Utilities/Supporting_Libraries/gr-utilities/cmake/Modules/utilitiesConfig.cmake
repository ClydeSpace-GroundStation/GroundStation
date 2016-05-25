INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_UTILITIES utilities)

FIND_PATH(
    UTILITIES_INCLUDE_DIRS
    NAMES utilities/api.h
    HINTS $ENV{UTILITIES_DIR}/include
        ${PC_UTILITIES_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    UTILITIES_LIBRARIES
    NAMES gnuradio-utilities
    HINTS $ENV{UTILITIES_DIR}/lib
        ${PC_UTILITIES_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(UTILITIES DEFAULT_MSG UTILITIES_LIBRARIES UTILITIES_INCLUDE_DIRS)
MARK_AS_ADVANCED(UTILITIES_LIBRARIES UTILITIES_INCLUDE_DIRS)

