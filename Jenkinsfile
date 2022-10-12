def tag_name = "latest"
if (env.TAG_NAME) {
    tag_name = "${env.TAG_NAME}"
}

def jobsMapping = [
    tags: [jobName:"App Gerlich Triplet Exploration", extraVars: "app_generic_image_tag: " + tag_name],
]

buildDockerImage([
    imageName: "triplet-exploration",
    pushRegistryNamespace: "gerlich",
    pushBranches: ['master'],
    tower: jobsMapping,
])
