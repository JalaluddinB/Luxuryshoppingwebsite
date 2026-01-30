package security.dockerfile

# Dockerfile Security Policy
# This policy ensures Dockerfile follows security best practices

import future.keywords.contains
import future.keywords.if
import future.keywords.in

# Check if Dockerfile uses specific base image
deny[msg] {
    input[i].Cmd == "from"
    val := input[i].Value
    not contains(val[0], ":")
    msg = sprintf("Base image '%s' should specify a version tag", [val[0]])
}

# Ensure non-root user is specified
deny[msg] {
    not user_defined
    msg = "Dockerfile should specify a non-root USER"
}

user_defined {
    input[_].Cmd == "user"
}

# Check for best practices
warn[msg] {
    input[i].Cmd == "run"
    val := concat(" ", input[i].Value)
    contains(val, "apt-get")
    not contains(val, "apt-get clean")
    not contains(val, "rm -rf /var/lib/apt/lists/*")
    msg = "apt-get used without cleanup, consider adding cleanup commands"
}

# Check HEALTHCHECK is defined
warn[msg] {
    not healthcheck_defined
    msg = "Consider adding a HEALTHCHECK instruction for better container monitoring"
}

healthcheck_defined {
    input[_].Cmd == "healthcheck"
}

# Prevent latest tag usage
deny[msg] {
    input[i].Cmd == "from"
    val := input[i].Value
    contains(val[0], ":latest")
    msg = sprintf("Avoid using 'latest' tag in base image '%s'", [val[0]])
}
