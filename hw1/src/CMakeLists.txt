cmake_minimum_required(VERSION 3.15)


add_subdirectory(tools)
add_subdirectory(lib/mongoose-cpp)
add_subdirectory(lib/json)
add_subdirectory(lib/yaml-cpp)
add_subdirectory(lib/avro-cpp-packaging)
add_subdirectory(lib/msgpack-c)

set (CMAKE_CXX_STANDARD 20)
add_executable(main main.cpp)
add_library(proxy proxy.cpp proxy.h)
add_library(tester SerializationTester.h SerializationTester.cpp)
add_library(serializers 
serializers/Serializer.h serializers/Serializer.cpp
serializers/NativeSerializer.h serializers/NativeSerializer.cpp
serializers/XMLSerializer.h serializers/XMLSerializer.cpp
serializers/JSONSerializer.h serializers/JSONSerializer.cpp
serializers/ProtoSerializer.h serializers/ProtoSerializer.cpp
serializers/YamlSerializer.h serializers/YamlSerializer.cpp
serializers/AvroSerializer.h serializers/AvroSerializer.cpp
serializers/MessagePackSerializer.h serializers/MessagePackSerializer.cpp)

project(serialization_tools_tester)

find_package(Boost COMPONENTS program_options serialization REQUIRED)
set(nlohmann_json_DIR "lib/json/build")
find_package(nlohmann_json REQUIRED)
find_package(yaml-cpp REQUIRED)


TARGET_LINK_LIBRARIES(main LINK_PUBLIC ${Boost_LIBRARIES})
TARGET_LINK_LIBRARIES(main LINK_PUBLIC tools)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC proxy)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC mongoose)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC serializers)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC tester)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC avrocpp)
TARGET_LINK_LIBRARIES(main LINK_PUBLIC yaml-cpp)
TARGET_LINK_LIBRARIES(tester LINK_PUBLIC tools serializers)
target_link_libraries(main LINK_PUBLIC msgpack-cxx)
TARGET_LINK_LIBRARIES(serializers LINK_PUBLIC nlohmann_json::nlohmann_json)
TARGET_LINK_LIBRARIES(serializers LINK_PUBLIC msgpack-cxx)

target_include_directories(main PRIVATE lib/mongoose-cpp)
target_include_directories(proxy PRIVATE lib/mongoose-cpp)
target_include_directories(serializers PRIVATE ${Boost_LIBRARIES})
target_include_directories(proxy PRIVATE serializers)

