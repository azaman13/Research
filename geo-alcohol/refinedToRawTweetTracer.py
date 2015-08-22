"""
Author: Anis Zaman

Description: Using tweetId, this is a helper module that associates refined tweet
(containing fewer info) to raw tweet data. Once an associated tweet
from the raw tweet file is found we save the raw tweet to a file
which later becomes the input of another script 
"""
import argparse
import json

def find_json_association(
        refined_file_name,
        original_file_name,
        lineIds_file,
        output_file_name):

    """
	@param:
	refined_file_name: Refined tweets file
	original_file_name: Original tweets file
	lineIds_file: File containing all the lineIds we are interested,
				thi is for the refined_file_name's line number (zero indexed)
	output_file_name: Name of the file where we dump the original tweets

	Given the following:
		- four file names, two of the files contains a valid json/line, one containing
		  lineIds and the outputFile name
		- 2 top level json fields that are associated by field values
	The function finds the associated json document (line) from the original_file_name
	and dumps the line/json in the output_file_name
	"""
    result = open(output_file_name,"w+")
    with open(original_file_name) as originalFile, \
            open(refined_file_name) as refinedFile, \
            open(lineIds_file) as lineIDs:
        tweets = refinedFile.read().split('\n')
        original_tweets = originalFile.read().split('\n')
        processed = 0
        for line_index in lineIDs:
            tweet = json.loads(tweets[int(line_index)])
            tweet_id = tweet.get('tweet')
            for original_tweet in original_tweets:
                    if original_tweet:
                        original_tweet = json.loads(original_tweet)
                        if original_tweet.get('id') == tweet_id:
                            json.dump(original_tweet, result)
                            result.write('\n')
                            print 'Done writing ' + str(processed)
                            processed += 1
    result.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Description of your program')
	parser.add_argument(
        '-r','--refined', help='Refined Tweet File Name', required=True
    )
	parser.add_argument(
        '-o','--original', help='Original Tweet File Name', required=True
    )
	parser.add_argument(
        '-f','--outputFile', help='Name of the outputFile', required=True
    )
	parser.add_argument(
        '-l','--lineIds', help='A File with lineIds in every line',
        required=True
    )
	args = vars(parser.parse_args())
	find_json_association(
        args.get('refined'), args.get('original'),
		args.get('lineIds'), args.get('outputFile')
	)