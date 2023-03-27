import AWS from "aws-sdk";

/**
 * Composable function for creating new DynamoDB instance based on specified region
 * @param {string} region
 * @returns AWS.DynamoDB instance
 */
export function useDynamoDB(region) {
	AWS.config.region = region;
	return new AWS.DynamoDB({ apiVersion: "2012-08-10" });
}
