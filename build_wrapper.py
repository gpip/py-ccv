import os

from cffi import FFI


ffi = FFI()
ffi.cdef("""
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
  CCV_IO_ANY_FILE = 0x020,
  ...
};

void ccv_disable_cache(void);
void ccv_enable_default_cache(void);

int ccv_read_impl(const char*, ccv_dense_matrix_t**, int, int, int, int);

ccv_scd_classifier_cascade_t* ccv_scd_classifier_cascade_read(const char*);
ccv_array_t* ccv_scd_detect_objects(ccv_dense_matrix_t*, ccv_scd_classifier_cascade_t**, int, ccv_scd_param_t);
void ccv_scd_classifier_cascade_free(ccv_scd_classifier_cascade_t* cascade);

void ccv_array_free(ccv_array_t*);
void ccv_matrix_free(ccv_matrix_t*);

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
res = ffi.compile()
print res
