# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ctrl_msgs.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ctrl_msgs.proto',
  package='ctrl_msgs',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0f\x63trl_msgs.proto\x12\tctrl_msgs\"*\n\x04\x43trl\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x01\x12\t\n\x01v\x18\x02 \x01(\x01\x12\t\n\x01w\x18\x03 \x01(\x01\x62\x06proto3')
)




_CTRL = _descriptor.Descriptor(
  name='Ctrl',
  full_name='ctrl_msgs.Ctrl',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='flag', full_name='ctrl_msgs.Ctrl.flag', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='v', full_name='ctrl_msgs.Ctrl.v', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='w', full_name='ctrl_msgs.Ctrl.w', index=2,
      number=3, type=1, cpp_type=5, label=1,
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
  serialized_start=30,
  serialized_end=72,
)

DESCRIPTOR.message_types_by_name['Ctrl'] = _CTRL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Ctrl = _reflection.GeneratedProtocolMessageType('Ctrl', (_message.Message,), {
  'DESCRIPTOR' : _CTRL,
  '__module__' : 'ctrl_msgs_pb2'
  # @@protoc_insertion_point(class_scope:ctrl_msgs.Ctrl)
  })
_sym_db.RegisterMessage(Ctrl)


# @@protoc_insertion_point(module_scope)