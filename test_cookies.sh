#! /usr/bin/env sh

# Test if each of the cookiecutters work without errors

# Initialize variables with default values
del_out_dir=true

# Parse command-line options
while getopts "k" opt; do
    case "$opt" in
        k)
            del_out_dir=false
            shift
            ;;
        *)
            echo "Usage: $0 [-k] [output directory]"
            exit 1
            ;;
    esac
done

if [ -n "$1" ]; then
    out_dir="$1"
else
    out_dir="/tmp/cookiecutter"
fi

test_failed=0

# Run cookiecutter for each of the nested cookiecutter templates
find . -maxdepth 1 -type d | grep -Ev "(\.$|\.git|\.venv|images|c|html|bare)" | xargs -tI {} cookiecutter {} -o $out_dir/{} --no-input || test_failed=$?

# Optionally delete or keep the files that cookiecutter generates
[ $del_out_dir = "true" ] && rm -rf -- $out_dir

exit $test_failed
