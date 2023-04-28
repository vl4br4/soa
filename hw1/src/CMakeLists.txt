cmake_minimum_required(VERSION 3.15)


add_subdirectory(tools)
add_subdirectory(lib/mongoose-cpp)

set (CMAKE_CXX_STANDARD 20)
add_executable(main main.cpp)
add_library(proxy proxy.cpp proxy.h)
add_library(tester SerializationTester.h SerializationTester.cpp)
add_library(serializers 
serializers/Serializer.h serializers/Serializer.cpp
serializers/NativeSerializer.h serializers/NativeSerializer.cpp)

project(serialization_tools_tester)

find_package(Boost COMPONENTS program_options serialization REQUIRED)

TARGET_LINK_LIBRARIES(main LINK_PUBLIC ${Boost_LIBRARIES} )
TARGET_LINK_LIBRARIES(main LINK_PUBLIC tools)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC proxy)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC mongoose)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC serializers)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC tester)
TARGET_LINK_LIBRARIES(tester LINK_PUBLIC tools serializers)

target_include_directories(main PRIVATE lib/mongoose-cpp)
target_include_directories(proxy PRIVATE lib/mongoose-cpp)
target_include_directories(serializers PRIVATE ${Boost_LIBRARIES})
target_include_directories(proxy PRIVATE serializers)
