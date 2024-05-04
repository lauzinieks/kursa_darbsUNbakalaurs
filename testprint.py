PROJECT_ID = "lumibakalaurs"  # @param {type:"string"}
REGION = "europe-north1"  # @param {type: "string"}
CLUSTER = "lumicluster"  # @param {type: "string"}
INSTANCE = "lumibachelortest3"  # @param {type: "string"}
DATABASE = "postgres"  # @param {type: "string"}
TABLE_NAME = "vectorembeddings"  # @param {type: "string"}

print("projects/" + PROJECT_ID + "/locations/" + REGION + "/clusters/" + CLUSTER + "/instances/" + INSTANCE)