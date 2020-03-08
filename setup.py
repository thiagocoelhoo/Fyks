from distutils.core import setup, Extension

def main():
    setup(name="eletric",
          version="1.0.0",
          description="Python interface for the physics calcs function",
          author="Rbbithy",
          author_email="thiago.coelho158@gmail.com",
          ext_modules=[Extension("eletric", ["include/rigidbodymethods.c"])])

if __name__ == "__main__":
    main()