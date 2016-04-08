import os

from cffi import FFI


ffi = FFI()
ffi.cdef("""
enum {
  CCV_8U  = 0x01000,
  CCV_32S = 0x02000,
  CCV_32F = 0x04000,
  CCV_64S = 0x08000,
  CCV_64F = 0x10000,
};

enum {
  CCV_C1 = 0x001,
  CCV_C2 = 0x002,
  CCV_C3 = 0x003,
  CCV_C4 = 0x004,
};

typedef struct {
  int width;
  int height;
} ccv_size_t;

typedef struct {
  int type;
  uint64_t sig;
  int refcount;
  int rnum;
  int size;
  int rsize;
  void* data;
} ccv_array_t;

typedef struct {
  int x;
  int y;
  int width;
  int height;
} ccv_rect_t;

typedef struct {
  int id;
  float confidence;
} ccv_classification_t;

typedef struct {
  int left;
  int top;
  int right;
  int bottom;
} ccv_margin_t;

typedef union {
  unsigned char* u8;
  int* i32;
  float* f32;
  int64_t* i64;
  double* f64;
} ccv_matrix_cell_t;

typedef struct {
  int type;
  uint64_t sig;
  int refcount;
  int rows;
  int cols;
  int step;
  union {
    unsigned char u8;
    int i32;
    float f32;
    int64_t i64;
    double f64;
    void* p;
  } tag;
  ccv_matrix_cell_t data;
} ccv_dense_matrix_t;

typedef struct {
  ccv_rect_t rect;
  int neighbors;
  ccv_classification_t classification;
} ccv_comp_t;

typedef struct {
  int sx[4];
  int sy[4];
  int dx[4];
  int dy[4];
  float bias;
  float w[32];
} ccv_scd_stump_feature_t;

typedef struct {
  int count;
  ccv_scd_stump_feature_t* features;
  float threshold;
} ccv_scd_stump_classifier_t;

typedef struct {
  int channel;
  int sx;
  int sy;
  int dx;
  int dy;
  float bias;
} ccv_scd_tree_feature_t;

typedef struct {
  int type;
  uint32_t pass;
  ccv_scd_stump_feature_t feature;
  ccv_scd_tree_feature_t node[3];
  float beta[6];
  float threshold;
} ccv_scd_decision_tree_t;

typedef struct {
  int count;
  ccv_margin_t margin;
  ccv_size_t size;
  ccv_scd_stump_classifier_t* classifiers;
  struct {
    int count;
    ccv_scd_decision_tree_t* tree;
  } decision;
} ccv_scd_classifier_cascade_t;

typedef struct {
  int min_neighbors;
  int step_through;
  int interval;
  ccv_size_t size;
} ccv_scd_param_t;

typedef void ccv_matrix_t;

//extern const ccv_scd_param_t ccv_scd_default_params;
extern ccv_scd_param_t ccv_scd_default_params;

enum {
  CCV_IO_GRAY      = 0x100,
  CCV_IO_RGB_COLOR = 0x300
};

enum {
  CCV_IO_ANY_STREAM     = 0x010,
  CCV_IO_BMP_STREAM     = 0x011,
  CCV_IO_JPEG_STREAM    = 0x012,
  CCV_IO_PNG_STREAM     = 0x013,
  CCV_IO_PLAIN_STREAM   = 0x014,
  CCV_IO_DEFLATE_STREAM = 0x015,
  CCV_IO_ANY_FILE       = 0x020,
  CCV_IO_BMP_FILE       = 0x021,
  CCV_IO_JPEG_FILE      = 0x022,
  CCV_IO_PNG_FILE       = 0x023,
  CCV_IO_BINARY_FILE    = 0x024,
  CCV_IO_ANY_RAW        = 0x040,
  CCV_IO_RGB_RAW        = 0x041,
  CCV_IO_RGBA_RAW       = 0x042,
  CCV_IO_ARGB_RAW       = 0x043,
  CCV_IO_BGR_RAW        = 0x044,
  CCV_IO_BGRA_RAW       = 0x045,
  CCV_IO_ABGR_RAW       = 0x046,
  CCV_IO_GRAY_RAW       = 0x047
};

enum {
  CCV_IO_FINAL = 0x00,
  CCV_IO_CONTINUE,
  CCV_IO_ERROR,
  CCV_IO_ATTEMPTED,
  CCV_IO_UNKNOWN
};

void ccv_disable_cache(void);
void ccv_enable_default_cache(void);

int ccv_read_impl(const char*, ccv_dense_matrix_t**, int, int, int, int);
int ccv_write(ccv_dense_matrix_t*, char*, int*, int, void*);

ccv_scd_classifier_cascade_t* ccv_scd_classifier_cascade_read(const char*);
ccv_array_t* ccv_scd_detect_objects(ccv_dense_matrix_t*, ccv_scd_classifier_cascade_t**, int, ccv_scd_param_t);
void ccv_scd_classifier_cascade_free(ccv_scd_classifier_cascade_t* cascade);

void ccv_array_free(ccv_array_t*);
void ccv_matrix_free(ccv_matrix_t*);

void ccv_visualize(ccv_matrix_t*, ccv_matrix_t**, int);

void ccv_sobel(ccv_dense_matrix_t*, ccv_dense_matrix_t**, int, int, int);
void ccv_gradient(ccv_dense_matrix_t*, ccv_dense_matrix_t**, int, ccv_dense_matrix_t**, int, int, int);


#define CCV_BBF_POINT_MAX 8

typedef struct {
  int interval;
  int min_neighbors;
  int flags;
  int accurate;
  ccv_size_t size;
} ccv_bbf_param_t;

typedef struct {
  int size;
  int px[CCV_BBF_POINT_MAX];
  int py[CCV_BBF_POINT_MAX];
  int pz[CCV_BBF_POINT_MAX];
  int nx[CCV_BBF_POINT_MAX];
  int ny[CCV_BBF_POINT_MAX];
  int nz[CCV_BBF_POINT_MAX];
} ccv_bbf_feature_t;

typedef struct {
  int count;
  float threshold;
  ccv_bbf_feature_t* feature;
  float* alpha;
} ccv_bbf_stage_classifier_t;

typedef struct {
  int count;
  ccv_size_t size;
  ccv_bbf_stage_classifier_t* stage_classifier;
} ccv_bbf_classifier_cascade_t;

ccv_bbf_classifier_cascade_t* ccv_bbf_read_classifier_cascade(const char*);
ccv_array_t* ccv_bbf_detect_objects(
    ccv_dense_matrix_t*, ccv_bbf_classifier_cascade_t**,
    int, ccv_bbf_param_t);
void ccv_bbf_classifier_cascade_free(ccv_bbf_classifier_cascade_t* cascade);

extern ccv_bbf_param_t ccv_bbf_default_params;
""")

ffi.set_source('_ccv', '#include <ccv.h>',
    include_dirs=[os.getenv('INCDIR') or '.'],
    library_dirs=[os.getenv('LIBDIR') or '.'],
    libraries=['ccv'])


if __name__ == "__main__":
    res = ffi.compile()
    print res
