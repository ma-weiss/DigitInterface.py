# SPDX-FileCopyrightText: 2022 Manuel Weiss <mweiss@bht-berlin.de>
#
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.0)

project(digit_interface)

# set(CMAKE_BUILD_TYPE Release)
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -pedantic -ansi -std=c++98")

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
)


add_library(llapi SHARED
    low_level_api_class.cpp
    lowlevelapi.cpp
    artl.c

)

set_target_properties(llapi PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})