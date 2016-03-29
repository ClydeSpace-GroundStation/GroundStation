# http://www.cmake.org/pipermail/cmake/2006-October/011446.html
# Modified to use pkg config and use standard var names

#
# Find the fec includes and library
#
# This module defines
# fec_INCLUDE_DIR, where to find tiff.h, etc.
# fec_LIBRARIES, the libraries to link against to use fec.
# fec_FOUND, If false, do not try to use fec.

INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_fec "fec")

FIND_PATH(fec_INCLUDE_DIRS
    NAMES fec/TestCase.h
    HINTS ${PC_fec_INCLUDE_DIR}
    ${CMAKE_INSTALL_PREFIX}/include
    PATHS
    /usr/local/include
    /usr/include
)

FIND_LIBRARY(fec_LIBRARIES
    NAMES fec
    HINTS ${PC_fec_LIBDIR}
    ${CMAKE_INSTALL_PREFIX}/lib
    ${CMAKE_INSTALL_PREFIX}/lib64
    PATHS
    ${fec_INCLUDE_DIRS}/../lib
    /usr/local/lib
    /usr/lib
)

LIST(APPEND fec_LIBRARIES ${CMAKE_DL_LIBS})

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(fec DEFAULT_MSG fec_LIBRARIES fec_INCLUDE_DIRS)
MARK_AS_ADVANCED(fec_LIBRARIES fec_INCLUDE_DIRS)
