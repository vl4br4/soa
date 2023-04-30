#include "AvroSerializer.h"
#include <string>

namespace avro {
template<> struct codec_traits<TestData> {
    static void encode(Encoder& e, const TestData& testData) {
        avro::encode(e, testData.IntField);
        avro::encode(e, testData.Int64Field);
        avro::encode(e, testData.Int64Field);
        avro::encode(e, testData.DoubleField);
        avro::encode(e, testData.StrField);
        avro::encode(e, testData.VectorField);
        avro::encode(e, testData.MapField);
    }
    static void decode(Decoder& d, TestData& testData) {
        avro::decode(d, testData.IntField);
        avro::decode(d, testData.Int64Field);
        avro::decode(d, testData.Int64Field);
        avro::decode(d, testData.DoubleField);
        avro::decode(d, testData.StrField);
        avro::decode(d, testData.VectorField);
        avro::decode(d, testData.MapField);
    }
};
} // namespace avro


std::unique_ptr<avro::OutputStream> out;

std::string AvroSerializer::Serialize(const TestData &testData) {
    out = avro::memoryOutputStream();
    avro::EncoderPtr e = avro::binaryEncoder();
    e->init(*out);
    avro::encode(*e, testData);
    return "not suitable for test framework, so we use global variable";
}

TestData AvroSerializer::Deserialize(const std::string& serializedData) {
    std::unique_ptr<avro::InputStream> in = avro::memoryInputStream(*out);
    avro::DecoderPtr d = avro::binaryDecoder();
    d->init(*in);
    TestData testData;
    avro::decode(*d, testData);
    return testData;
}