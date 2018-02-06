python_binary(
    name = 'devils_tower',
    main = 'devils_tower.py',
    deps = [
        ':mock_trafficlights',
        ':jenkins',
        '//third_party:absl'
    ],
)

python_library(
    name = 'mock_trafficlights',
    srcs = ['mock_trafficlight.py'],
    deps = ['//third_party:absl'],
)

python_library(
    name = 'trafficlight',
    srcs = ['trafficlight.py'],
)

python_library(
    name = 'jenkins',
    srcs = ['jenkins.py'],
)
