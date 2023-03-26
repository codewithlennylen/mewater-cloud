<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/codewithlennylen/mewater-cloud">
    <img src="Architecture Docs/favicon.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">MeWater</h3>

  <p align="center">
    MeWater is a water conservation solution that uses IoT Devices (Solenoid Valves, Flow Meters, etc) to detect and monitor water leakages in realtime. The system auto-shuts down detected leakage lines thus saving on water.
    <br />
    <a href="https://github.com/codewithlennylen/mewater-cloud"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/codewithlennylen/mewater-cloud">View Demo</a>
    ·
    <a href="https://github.com/codewithlennylen/mewater-cloud/issues">Report Bug</a>
    ·
    <a href="https://github.com/codewithlennylen/mewater-cloud/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

<br/>

<div align="center">
  <a href="https://github.com/codewithlennylen/mewater-cloud">
    <img src="Architecture Docs/mewater-iot.jpg">
  </a>
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![AWS][AWS]][aws-url]
* [![Python][Python]][Python-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

I would ideally share this architecture via Infrastructure as Code such as AWS Cloudformation or Terraform. But I'll deliver that sometime in the future as I iterate and improve on the architecture.

<div align="center">
  <a href="https://github.com/codewithlennylen/mewater-cloud">
    <img src="Architecture Docs/mewater-data-pipeline.drawio.png">
  </a>
</div>

<br/>

There are 4 major functions that this architecture serves:

1. Getting IoT Data from IoT Core and Storing it in an S3 Bucket (Raw)
2. Processing the raw data into something useful to display to end-users
3. Sending alerts to users in case a leak is detected
4. Sending 'valve shutdown' command to IoT Devices in case a leak is detected

<br/>

### 1. Storing Raw Data

We use an IoT rule provided by AWS IoT Core to push data from a subscribed MQTT topic to an S3 Bucket.

<br/>

### 2. Data Processing & Data Display

A lambda function sits at the heart of our solution. It takes the data from S3 via a trigger event (anytime data is pushed into the bucket, it's immediately processed) -> we were aiming for a realtime solution

The processed data is stored in a DynamoDB Table, which allows for near-realtime queries.

We've then set up an EC2 Instance to serve our web application where users can view a live dashboard allowing them to monitor the system status. The web-app access our DynamoDB Table via the Python Boto3 SDK.

<div align="center">
  <a href="#">
    <img src="#" alt="MeWater Dashboard Screenshot">
  </a>
</div>

<br/>

### 3. Leakage Detection Algorithm & User Alerts

The current leakage detection algorithm is a poor man's version, in that we only subtract output water volumes from the input. We are working on a more sophisticated algorithm.

```
leaked_volume = inlet_volume - (outlet1_volume + outlet2_volume)
```

Once a leakage is detected, the lambda pushes a message with the leakage info to an AWS SNS Topic.

* Another Lambda function is subscribed to this topic and this function sends a command to the IoT Devices via AWS IoT Core to shutdown the valves thus stopping the water leak
* An SMS is sent to the user informing them of the detected leak
* An Email is sent to the user informing them of the detected leak

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

* [ ] Use AWS Secrets Manager to securely store environment variables
* [ ] Use Kinesis Data Analytics to analyze IoT realtime events
* [ ] Build an API to query the Raw Data -> AWS API Gateway

See the [open issues](https://github.com/codewithlennylen/mewater-cloud/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Lenny Ng'ang'a - [@codewithlenny](https://twitter.com/codewithlenny) - codewithlennylen254@gmail.com

Project Link: [https://github.com/codewithlennylen/mewater-cloud](https://github.com/codewithlennylen/mewater-cloud)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Fanuel Conrad](https://github.com/FanuelConrad) - IoT Lead

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/codewithlennylen/mewater-cloud.svg?style=for-the-badge
[contributors-url]: https://github.com/codewithlennylen/mewater-cloud/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/codewithlennylen/mewater-cloud.svg?style=for-the-badge
[forks-url]: https://github.com/codewithlennylen/mewater-cloud/network/members
[stars-shield]: https://img.shields.io/github/stars/codewithlennylen/mewater-cloud.svg?style=for-the-badge
[stars-url]: https://github.com/codewithlennylen/mewater-cloud/stargazers
[issues-shield]: https://img.shields.io/github/issues/codewithlennylen/mewater-cloud.svg?style=for-the-badge
[issues-url]: https://github.com/codewithlennylen/mewater-cloud/issues
[license-shield]: https://img.shields.io/github/license/codewithlennylen/mewater-cloud.svg?style=for-the-badge
[license-url]: https://github.com/codewithlennylen/mewater-cloud/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/lenny-nganga-wanjiru
[product-screenshot]: images/screenshot.png
[AWS]: https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white
[aws-url]: https://aws.amazon.com/
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/