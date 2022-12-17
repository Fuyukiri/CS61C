from distutils.core import setup, Extension
import sysconfig

def main():
    CFLAGS = ['-g', '-Wall', '-std=c99', '-fopenmp', '-mavx', '-mfma', '-pthread', '-O3']
    LDFLAGS = ['-fopenmp']
    setup(name="numc",
          version="0.0.1",
          description="numc matrix operations",
          ext_modules=[
            Extension("numc",
                      sources=["src/numc.c", "src/matrix.c"],
                      extra_compile_args=CFLAGS,
                      extra_link_args=LDFLAGS,
                      language='c')
          ])


if __name__ == "__main__":
    main()
