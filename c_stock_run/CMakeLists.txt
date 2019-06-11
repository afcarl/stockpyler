# CMakeList.txt : CMake project for c_stock_run, include source and define
# project specific logic here.
#
cmake_minimum_required (VERSION 3.8)

set (CMAKE_CXX_STANDARD 17)


# Add source to this project's executable.

file( GLOB LIB_SOURCES *.cpp )
file( GLOB LIB_HEADERS *.h )

set (SOURCES history_manager.cpp main.cpp Observer.cpp position_manager.cpp rff_tools.cpp Stockpyler.cpp Strategy.cpp)
set (HEADERS history_manager.hpp Observer.hpp position_manager.hpp rff_tools.hpp Stockpyler.hpp Strategy.hpp)


add_executable (c_stock_run ${SOURCES} ${HEADERS})

# TODO: Add tests and install targets if needed.
