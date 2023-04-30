#include "MessagePackSerializer.h"
#include <string>
#include <iostream>

struct DataForMessagePack : public TestData {
    DataForMessagePack() = default;
    DataForMessagePack(TestData testData)
    : TestData(std::move(testData)) {}
    MSGPACK_DEFINE(IntField, Int64Field, DoubleField, StrField, VectorField, MapField);
};

namespace msgpack {
MSGPACK_API_VERSION_NAMESPACE(MSGPACK_DEFAULT_API_NS) {
namespace adaptor {

template<>
struct as<DataForMessagePack> {
    DataForMessagePack operator()(msgpack::object const& o) const {
        return TestData(
            o.via.array.ptr[0].as<int>(),
            o.via.array.ptr[1].as<int64_t>(),
            o.via.array.ptr[2].as<double>(),
            o.via.array.ptr[3].as<std::string>(),
            o.via.array.ptr[4].as<std::vector<int>>(),
            o.via.array.ptr[5].as<std::map<std::string, int>>()
        );
    }
};

} // namespace adaptor
} // MSGPACK_API_VERSION_NAMESPACE(MSGPACK_DEFAULT_API_NS)
} // namespace msgpack

std::string MessagePackSerializer::Serialize(const TestData &testData) {
    std::stringstream ss;
    msgpack::pack(ss, DataForMessagePack(testData));
    return ss.str();
}

TestData MessagePackSerializer::Deserialize(const std::string& serializedData) {
    auto oh = msgpack::unpack(serializedData.data(), serializedData.size());
    auto obj = oh.get();
    return obj.as<DataForMessagePack>();
}