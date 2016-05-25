INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_TNC tnc)

FIND_PATH(
    TNC_INCLUDE_DIRS
    NAMES tnc/api.h
    HINTS $ENV{TNC_DIR}/include
        ${PC_TNC_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREEFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    TNC_LIBRARIES
    NAMES gnuradio-tnc
    HINTS $ENV{TNC_DIR}/lib
        ${PC_TNC_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(TNC DEFAULT_MSG TNC_LIBRARIES TNC_INCLUDE_DIRS)
MARK_AS_ADVANCED(TNC_LIBRARIES TNC_INCLUDE_DIRS)

