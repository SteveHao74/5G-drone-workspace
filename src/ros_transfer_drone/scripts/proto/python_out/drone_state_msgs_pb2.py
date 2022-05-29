# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: drone_state_msgs.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='drone_state_msgs.proto',
  package='drone_state_msgs',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x16\x64rone_state_msgs.proto\x12\x10\x64rone_state_msgs\"T\n\nDroneState\x12\"\n\x03gps\x18\x01 \x01(\x0b\x32\x15.drone_state_msgs.GPS\x12\"\n\x03imu\x18\x02 \x01(\x0b\x32\x15.drone_state_msgs.IMU\"V\n\x03GPS\x12\r\n\x05lon_x\x18\x01 \x01(\x01\x12\r\n\x05lat_y\x18\x02 \x01(\x01\x12\r\n\x05\x61lt_z\x18\x03 \x01(\x01\x12\n\n\x02vx\x18\x04 \x01(\x01\x12\n\n\x02vy\x18\x05 \x01(\x01\x12\n\n\x02vz\x18\x06 \x01(\x01\"l\n\x03IMU\x12\x0e\n\x06quan_x\x18\x01 \x01(\x01\x12\x0e\n\x06quan_y\x18\x02 \x01(\x01\x12\x0e\n\x06quan_z\x18\x03 \x01(\x01\x12\x0e\n\x06quan_w\x18\x04 \x01(\x01\x12\x0b\n\x03w_x\x18\x05 \x01(\x01\x12\x0b\n\x03w_y\x18\x06 \x01(\x01\x12\x0b\n\x03w_z\x18\x07 \x01(\x01\x62\x06proto3')
)




_DRONESTATE = _descriptor.Descriptor(
  name='DroneState',
  full_name='drone_state_msgs.DroneState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gps', full_name='drone_state_msgs.DroneState.gps', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='imu', full_name='drone_state_msgs.DroneState.imu', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=44,
  serialized_end=128,
)


_GPS = _descriptor.Descriptor(
  name='GPS',
  full_name='drone_state_msgs.GPS',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='lon_x', full_name='drone_state_msgs.GPS.lon_x', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lat_y', full_name='drone_state_msgs.GPS.lat_y', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='alt_z', full_name='drone_state_msgs.GPS.alt_z', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vx', full_name='drone_state_msgs.GPS.vx', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vy', full_name='drone_state_msgs.GPS.vy', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vz', full_name='drone_state_msgs.GPS.vz', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=130,
  serialized_end=216,
)


_IMU = _descriptor.Descriptor(
  name='IMU',
  full_name='drone_state_msgs.IMU',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='quan_x', full_name='drone_state_msgs.IMU.quan_x', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='quan_y', full_name='drone_state_msgs.IMU.quan_y', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='quan_z', full_name='drone_state_msgs.IMU.quan_z', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='quan_w', full_name='drone_state_msgs.IMU.quan_w', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='w_x', full_name='drone_state_msgs.IMU.w_x', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='w_y', full_name='drone_state_msgs.IMU.w_y', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='w_z', full_name='drone_state_msgs.IMU.w_z', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=218,
  serialized_end=326,
)

_DRONESTATE.fields_by_name['gps'].message_type = _GPS
_DRONESTATE.fields_by_name['imu'].message_type = _IMU
DESCRIPTOR.message_types_by_name['DroneState'] = _DRONESTATE
DESCRIPTOR.message_types_by_name['GPS'] = _GPS
DESCRIPTOR.message_types_by_name['IMU'] = _IMU
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DroneState = _reflection.GeneratedProtocolMessageType('DroneState', (_message.Message,), {
  'DESCRIPTOR' : _DRONESTATE,
  '__module__' : 'drone_state_msgs_pb2'
  # @@protoc_insertion_point(class_scope:drone_state_msgs.DroneState)
  })
_sym_db.RegisterMessage(DroneState)

GPS = _reflection.GeneratedProtocolMessageType('GPS', (_message.Message,), {
  'DESCRIPTOR' : _GPS,
  '__module__' : 'drone_state_msgs_pb2'
  # @@protoc_insertion_point(class_scope:drone_state_msgs.GPS)
  })
_sym_db.RegisterMessage(GPS)

IMU = _reflection.GeneratedProtocolMessageType('IMU', (_message.Message,), {
  'DESCRIPTOR' : _IMU,
  '__module__' : 'drone_state_msgs_pb2'
  # @@protoc_insertion_point(class_scope:drone_state_msgs.IMU)
  })
_sym_db.RegisterMessage(IMU)


# @@protoc_insertion_point(module_scope)
