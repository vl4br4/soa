cmake_minimum_required(VERSION 3.15)


add_subdirectory(tools)
add_subdirectory(lib/mongoose-cpp)
add_subdirectory(lib/json)
add_subdirectory(lib/protobuf)

set (CMAKE_CXX_STANDARD 20)
add_executable(main main.cpp)
add_library(proxy proxy.cpp proxy.h)
add_library(tester SerializationTester.h SerializationTester.cpp)
add_library(serializers 
serializers/Serializer.h serializers/Serializer.cpp
serializers/NativeSerializer.h serializers/NativeSerializer.cpp
serializers/XMLSerializer.h serializers/XMLSerializer.cpp
serializers/JSONSerializer.h serializers/JSONSerializer.cpp
serializers/ProtoSerializer.h serializers/ProtoSerializer.cpp)


project(serialization_tools_tester)

find_package(Boost COMPONENTS program_options serialization REQUIRED)
set(nlohmann_json_DIR "lib/json/build")
find_package(nlohmann_json REQUIRED)

find_package(Protobuf REQUIRED)

add_library(protos lib/protos/test_data.pb.cc lib/protos/test_data.pb.h)
TARGET_LINK_LIBRARIES(protos LINK_PUBLIC protobuf)


TARGET_LINK_LIBRARIES(main LINK_PUBLIC ${Boost_LIBRARIES})
TARGET_LINK_LIBRARIES(main LINK_PUBLIC tools)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC proxy)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC mongoose)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC serializers)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC tester)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC protos)
TARGET_LINK_LIBRARIES(tester LINK_PUBLIC tools serializers)
TARGET_LINK_LIBRARIES(serializers LINK_PUBLIC nlohmann_json::nlohmann_json)
TARGET_LINK_LIBRARIES(serializers LINK_PUBLIC protos)

target_include_directories(main PRIVATE lib/mongoose-cpp)
target_include_directories(main PRIVATE protos)
target_include_directories(proxy PRIVATE lib/mongoose-cpp)
target_include_directories(serializers PRIVATE ${Boost_LIBRARIES})
target_include_directories(proxy PRIVATE serializers)
target_include_directories(protos PRIVATE protobuf)
