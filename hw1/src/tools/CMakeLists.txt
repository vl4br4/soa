cmake_minimum_required(VERSION 3.15)

set (CMAKE_CXX_STANDARD 20)

project(tools)

add_library(tools tick.h tick.cpp)