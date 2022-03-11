import urllib, boto3

s3 = boto3.client('s3')

instructions_object = s3.get_object(Bucket='bad-math-ctf',Key='system/instructions.txt')
instructions_html_comment = instructions_object['Body'].read().decode('utf-8')

def get_hint(event, context):
    html_body = """
    <h1>hint</h1>
    <p>add "debug=True" to /calculator POST body</p>
    """
    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},
        "body": html_body
    }

def handle_calculator_http(event, context):
    if event['httpMethod'] == "GET":
        print("running get_calculator")
        return get_calculator()
    elif event['httpMethod'] == "POST":
        http_post = dict(param.split("=") for param in event['body'].split("&"))
        submission = urllib.parse.unquote(http_post['submission'])
    
        # threat intel
        print(event['requestContext']['identity']['sourceIp'] + " submitted " + submission)
        
        # debug enabled?
        debug = event['body'].get('debug') if type(event['body']) == dict else False
        
        return do_math(submission, debug)

def get_calculator():
    html_body = """
    {}
    <h1>unhackable calculator</h1>
    <form action="calculator" method="post">
        <label for="submission">what would you like us to calculate?</label><br>
        <input type="text" id="submission" name="submission"><br>
    </form> 
    """.format(instructions_html_comment)
    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},
        "body": html_body
    }

def do_math(submission, debug=False):
    try:
        result = eval(submission)
    except Exception as e:
        if debug:
            result = e
        pass
    # TODO - pass logs to the math institute DB, needs math-institute-key from SSM 
    html_body = """
    <h1>unhackable calculator</h1>
    <h3>result: {}
    <form action="calculator" method="post">
        <label for="submission">what would you like us to calculate?</label><br>
        <input type="text" id="submission" name="submission"><br>
    </form> 
    """.format(result)

    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},
        "body": html_body
    }