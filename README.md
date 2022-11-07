
# ECS Fargate Website using AWS CDK

This project is a template which allows you to deploy the infrastructure required on AWS, to host an image pulled from a repository. Here we are using **coderaiser/cloudcmd:latest**

Resource links: 
- https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html
- https://github.com/neiltesaluna/aws-cdk-getting-started

You can declare the image you want to spin up in:  
**ecs_website/ecs_website_stack.py**.
```
ecs_taskdefinition.add_container("ecsContainer",
    image=aws_ecs.ContainerImage.from_registry('coderaiser/cloudcmd:latest'), # change image here
    cpu=256,
    memory_limit_mib=512,
    port_mappings=[aws_ecs.PortMapping(container_port=8000)]
)
```

*Note this repository assumes that you have installed [AWS CLI](https://aws.amazon.com/cli/), so that your AWS Account will be used for deployment.* 

## Setting up the environment
To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
(.venv) username > pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
(.venv) username > cdk synth
```

You can also check out the CloudFormation template generated using `cdk synth` in the JSON file below:  
**cdk.out/EcsWebsiteStack.template.json**


## Deploying the website on AWS

Now that all the dependencies are installed for AWS CDK to deploy on AWS. Run the following command:

```
(.venv) username > cdk deploy
```

## Useful Information

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

### More Commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

