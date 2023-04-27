from distutils.core import setup


setup(
    name = 'md5_task_data',
    version = '0.0.0',
    description = 'CRUD ops for MD5 task data',
    author='Akim Mukhtarov',
    author_email = 'akim.int80h@gmail.com',
    packages = [
        'md5_task_data',
        ],
    install_requires = [
        'asyncpg==0.27.0',
        'greenlet==2.0.2',
        'psycopg2-binary==2.9.6',
        'pydantic==1.10.7',
        'SQLAlchemy==2.0.10',
        'typing_extensions==4.5.0'
        ],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        ],
)
