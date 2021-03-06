# -*- coding: utf-8 -*-

"""
Dummy MPI
=========
Dummy module that emulates the functionality of the :mod:`mpi4py.MPI` module.
It is automatically imported as :mod:`mpi4pyd.MPI` if :mod:`mpi4py.MPI` is not
available.
This is a specialized version of the `mpi_dummy` package available at
https://gitlab.mpcdf.mpg.de/ift/mpi_dummy

"""


# %% IMPORTS
# Built-in imports
from copy import deepcopy as copy
from pkg_resources import parse_version

# Package imports
import numpy as np

# mpi4pyd imports
from mpi4pyd import __version__

# All declaration
__all__ = ['COMM_SELF', 'COMM_WORLD', 'Comm', 'Datatype', 'Intracomm', 'Op',
           'AINT', 'BAND', 'BOOL', 'BOR', 'BXOR', 'BYTE', 'CHAR', 'CHARACTER',
           'COMPLEX', 'COMPLEX16', 'COMPLEX32', 'COMPLEX4', 'COMPLEX8',
           'COUNT', 'CXX_BOOL', 'CXX_DOUBLE_COMPLEX', 'CXX_FLOAT_COMPLEX',
           'CXX_LONG_DOUBLE_COMPLEX', 'C_BOOL', 'C_COMPLEX',
           'C_DOUBLE_COMPLEX', 'C_FLOAT_COMPLEX', 'C_LONG_DOUBLE_COMPLEX',
           'DATATYPE_NULL', 'DOUBLE', 'DOUBLE_COMPLEX', 'DOUBLE_INT',
           'DOUBLE_PRECISION', 'FLOAT', 'FLOAT_INT', 'F_BOOL', 'F_COMPLEX',
           'F_DOUBLE', 'F_DOUBLE_COMPLEX', 'F_FLOAT', 'F_FLOAT_COMPLEX',
           'F_INT', 'INT', 'INT16_T', 'INT32_T', 'INT64_T', 'INT8_T',
           'INTEGER', 'INTEGER1', 'INTEGER16', 'INTEGER2', 'INTEGER4',
           'INTEGER8', 'INT_INT', 'LAND', 'LB', 'LOGICAL', 'LOGICAL1',
           'LOGICAL2', 'LOGICAL4', 'LOGICAL8', 'LONG', 'LONG_DOUBLE',
           'LONG_DOUBLE_INT', 'LONG_INT', 'LONG_LONG', 'LOR', 'LXOR', 'OFFSET',
           'MAX', 'MAXLOC', 'MIN', 'MINLOC', 'NO_OP', 'OP_NULL', 'PACKED',
           'PROD', 'REAL', 'REAL16', 'REAL2', 'REAL4', 'REAL8', 'REPLACE',
           'SHORT', 'SHORT_INT', 'SIGNED_CHAR', 'SIGNED_INT', 'SIGNED_LONG',
           'SIGNED_LONG_LONG', 'SIGNED_SHORT', 'SINT16_T', 'SINT32_T',
           'SINT64_T', 'SINT8_T', 'SUM', 'TWOINT', 'UB', 'UINT16_T',
           'UINT32_T', 'UINT64_T', 'UINT8_T', 'UNSIGNED', 'UNSIGNED_CHAR',
           'UNSIGNED_INT', 'UNSIGNED_LONG', 'UNSIGNED_LONG_LONG',
           'UNSIGNED_SHORT', 'WCHAR', 'ANY_SOURCE', 'ANY_TAG', 'get_vendor']


# %% COMM CLASS DEFINITION
# Make dummy Comm class
class Comm(object):
    def __init__(self):
        # Save name of this class if not saved already
        if not hasattr(self, '_name'):
            self.name = "dummyMPI_%s" % (self.__class__.__name__)
        # If it was saved, check that it starts with 'dummyMPI_'
        elif not self._name.startswith('dummyMPI_'):
            # If not, add it
            self._name = "dummyMPI_%s" % (self._name)

        # Save rank and size of communicator
        self._rank = 0
        self._size = 1

    # %% CLASS PROPERTIES
    @property
    def name(self):
        return(self._name)

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError("Input argument 'name' is not of type 'str'!")

    @property
    def rank(self):
        return(self._rank)

    @property
    def size(self):
        return(self._size)

    # %% GENERAL CLASS METHODS
    def _get_buffer(self, buff):
        # If buff is a list or tuple, return the first element
        if isinstance(buff, (list, tuple)):
            return(buff[0])
        # Else, return buff itself
        else:
            return(buff)

    def _scatter_gather(self, sendbuf, recvbuf=None):
        # Unwrap the sending and receiving buffers
        sendbuf = self._get_buffer(sendbuf)
        recvbuf = self._get_buffer(recvbuf)

        # If no receiving buffer was supplied, return a copy of sendbuf
        if recvbuf is None:
            # Make a copy of sendbuf
            return(copy(sendbuf))
        # If a receiving buffer was supplied, use it
        else:
            recvbuf[:] = sendbuf
            return(recvbuf)

    # %% VISIBLE CLASS METHODS
    # TODO: Implement dummy versions of missing communication methods
    # Still missing: Alltoall and non-blocking/synchronous (I/S) methods
    def Get_name(self):
        return(self.name)

    def Get_rank(self):
        return(self.rank)

    def Get_size(self):
        return(self.size)

    def Allgather(self, sendbuf, recvbuf, *args, **kwargs):
        return(self.Gather(sendbuf, recvbuf))

    def allgather(self, sendobj, *args, **kwargs):
        return(self.gather(sendobj))

    def Allgatherv(self, sendbuf, recvbuf, *args, **kwargs):
        return(self.Gatherv(sendbuf, recvbuf))

    def Allreduce(self, sendbuf, recvbuf, *args, **kwargs):
        return(self.Reduce(sendbuf, recvbuf))

    def allreduce(self, sendobj, *args, **kwargs):
        return(self.reduce(sendobj))

    def Barrier(self):
        pass

    def barrier(self):
        pass

    def Bcast(self, buf, *args, **kwargs):
        return(buf)

    def bcast(self, obj, *args, **kwargs):
        return(obj)

    def Gather(self, sendbuf, recvbuf, *args, **kwargs):
        return(self._scatter_gather(sendbuf, recvbuf))

    def gather(self, sendobj, *args, **kwargs):
        return([sendobj])

    def Gatherv(self, sendbuf, recvbuf, *args, **kwargs):
        return(self._scatter_gather(sendbuf, recvbuf))

    def Is_intra(self):
        return(isinstance(self, Intracomm))

    def Is_inter(self):
        return(False)

    def Reduce(self, sendbuf, recvbuf, *args, **kwargs):
        return(self._scatter_gather(sendbuf, recvbuf))

    def reduce(self, sendobj, *args, **kwargs):
        if np.isscalar(sendobj):
            return(sendobj)
        else:
            return(self._scatter_gather(sendobj))

    def Scatter(self, sendbuf, recvbuf, *args, **kwargs):
        return(self._scatter_gather(sendbuf, recvbuf))

    def scatter(self, sendobj, *args, **kwargs):
        return(sendobj[0])

    def Scatterv(self, sendbuf, recvbuf, *args, **kwargs):
        return(self._scatter_gather(sendbuf, recvbuf))

    def Sendrecv(self, sendbuf, *args, **kwargs):
        return(sendbuf)

    def sendrecv(self, sendobj, *args, **kwargs):
        return(sendobj)


# %% INTRACOMM CLASS DEFINITION
# Make dummy Intracomm class
class Intracomm(Comm):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        super(Intracomm, self).__init__(*args, **kwargs)


# %% INITIALIZE COMM_WORLD AND COMM_SELF
COMM_WORLD = Intracomm('dummyMPI_COMM_WORLD')
COMM_SELF = Intracomm('dummyMPI_COMM_SELF')


# %% DATATYPE DEFINITIONS
# Make dummy Datatype class
class Datatype(object):
    def __init__(self, name):
        self.name = name


# MPI standard datatypes
AINT = Datatype('dummyMPI_AINT')
BYTE = Datatype('dummyMPI_BYTE')
CHAR = Datatype('dummyMPI_CHAR')
CHARACTER = Datatype('dummyMPI_CHARACTER')
COMPLEX = Datatype('dummyMPI_COMPLEX')
COMPLEX4 = Datatype('dummyMPI_COMPLEX4')
COMPLEX8 = Datatype('dummyMPI_COMPLEX8')
COMPLEX16 = Datatype('dummyMPI_COMPLEX16')
COMPLEX32 = Datatype('dummyMPI_COMPLEX32')
COUNT = Datatype('dummyMPI_COUNT')
CXX_BOOL = Datatype('dummyMPI_CXX_BOOL')
CXX_DOUBLE_COMPLEX = Datatype('dummyMPI_CXX_DOUBLE_COMPLEX')
CXX_FLOAT_COMPLEX = Datatype('dummyMPI_CXX_FLOAT_COMPLEX')
CXX_LONG_DOUBLE_COMPLEX = Datatype('dummyMPI_CXX_LONG_DOUBLE_COMPLEX')
C_BOOL = Datatype('dummyMPI_C_BOOL')
C_COMPLEX = Datatype('dummyMPI_C_COMPLEX')
C_DOUBLE_COMPLEX = Datatype('dummyMPI_C_DOUBLE_COMPLEX')
C_FLOAT_COMPLEX = Datatype('dummyMPI_C_FLOAT_COMPLEX')
C_LONG_DOUBLE_COMPLEX = Datatype('dummyMPI_C_LONG_DOUBLE_COMPLEX')
DATATYPE_NULL = Datatype('dummyMPI_DATATYPE_NULL')
DOUBLE = Datatype('dummyMPI_DOUBLE')
DOUBLE_COMPLEX = Datatype('dummyMPI_DOUBLE_COMPLEX')
DOUBLE_INT = Datatype('dummyMPI_DOUBLE_INT')
DOUBLE_PRECISION = Datatype('dummyMPI_DOUBLE_PRECISION')
FLOAT = Datatype('dummyMPI_FLOAT')
FLOAT_INT = Datatype('dummyMPI_FLOAT_INT')
INT = Datatype('dummyMPI_INT')
INT8_T = Datatype('dummyMPI_INT8_T')
INT16_T = Datatype('dummyMPI_INT16_T')
INT32_T = Datatype('dummyMPI_INT32_T')
INT64_T = Datatype('dummyMPI_INT64_T')
INTEGER = Datatype('dummyMPI_INTEGER')
INTEGER1 = Datatype('dummyMPI_INTEGER1')
INTEGER2 = Datatype('dummyMPI_INTEGER2')
INTEGER4 = Datatype('dummyMPI_INTEGER4')
INTEGER8 = Datatype('dummyMPI_INTEGER8')
INTEGER16 = Datatype('dummyMPI_INTEGER16')
INT_INT = Datatype('dummyMPI_2INT')
LB = Datatype('dummyMPI_LB')
LOGICAL = Datatype('dummyMPI_LOGICAL')
LOGICAL1 = Datatype('dummyMPI_LOGICAL1')
LOGICAL2 = Datatype('dummyMPI_LOGICAL2')
LOGICAL4 = Datatype('dummyMPI_LOGICAL4')
LOGICAL8 = Datatype('dummyMPI_LOGICAL8')
LONG = Datatype('dummyMPI_LONG')
LONG_DOUBLE = Datatype('dummyMPI_LONG_DOUBLE')
LONG_DOUBLE_INT = Datatype('dummyMPI_LONG_DOUBLE_INT')
LONG_INT = Datatype('dummyMPI_LONG_INT')
LONG_LONG = Datatype('dummyMPI_LONG_LONG_INT')
OFFSET = Datatype('dummyMPI_OFFSET')
PACKED = Datatype('dummyMPI_PACKED')
REAL = Datatype('dummyMPI_REAL')
REAL2 = Datatype('dummyMPI_REAL2')
REAL4 = Datatype('dummyMPI_REAL4')
REAL8 = Datatype('dummyMPI_REAL8')
REAL16 = Datatype('dummyMPI_REAL16')
SHORT = Datatype('dummyMPI_SHORT')
SHORT_INT = Datatype('dummyMPI_SHORT_INT')
SIGNED_CHAR = Datatype('dummyMPI_SIGNED_CHAR')
UB = Datatype('dummyMPI_UB')
UINT8_T = Datatype('dummyMPI_UINT8_T')
UINT16_T = Datatype('dummyMPI_UINT16_T')
UINT32_T = Datatype('dummyMPI_UINT32_T')
UINT64_T = Datatype('dummyMPI_UINT64_T')
UNSIGNED = Datatype('dummyMPI_UNSIGNED')
UNSIGNED_CHAR = Datatype('dummyMPI_UNSIGNED_CHAR')
UNSIGNED_LONG = Datatype('dummyMPI_UNSIGNED_LONG')
UNSIGNED_LONG_LONG = Datatype('dummyMPI_UNSIGNED_LONG_LONG')
UNSIGNED_SHORT = Datatype('dummyMPI_UNSIGNED_SHORT')
WCHAR = Datatype('dummyMPI_WCHAR')

# MPI datatype synonyms
BOOL = C_BOOL
F_BOOL = LOGICAL
F_COMPLEX = COMPLEX
F_DOUBLE = DOUBLE_PRECISION
F_DOUBLE_COMPLEX = DOUBLE_COMPLEX
F_FLOAT = REAL
F_FLOAT_COMPLEX = COMPLEX
F_INT = INTEGER
SIGNED_INT = INT
SIGNED_LONG = LONG
SIGNED_LONG_LONG = LONG_LONG
SIGNED_SHORT = SHORT
SINT8_T = INT8_T
SINT16_T = INT16_T
SINT32_T = INT32_T
SINT64_T = INT64_T
TWOINT = INT_INT
UNSIGNED_INT = UNSIGNED


# %% OPERATOR DEFINITIONS
# Make dummy Op class
class Op(object):
    def __init__(self, *args, **kwargs):
        self.is_predefined = True

    def __call__(self, *args, **kwargs):
        pass


# MPI standard operators
BAND = Op()
BOR = Op()
BXOR = Op()
LAND = Op()
LOR = Op()
LXOR = Op()
MAX = Op()
MAXLOC = Op()
MIN = Op()
MINLOC = Op()
NO_OP = Op()
OP_NULL = Op()
PROD = Op()
REPLACE = Op()
SUM = Op()


# %% MISCELLANEOUS
ANY_SOURCE = -2
ANY_TAG = -1


# %% DUMMY FUNCTIONS
def get_vendor():
    return("dummyMPI", parse_version(__version__)._version.release)
