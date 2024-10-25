rm *.whl
pip wheel . --no-deps
twine upload *.whl
rm *.whl
rm -r build
rm -r src/*.egg-info
