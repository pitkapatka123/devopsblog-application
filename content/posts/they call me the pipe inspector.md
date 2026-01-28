title: they call me the pipe inspector
date: 2026-01-26
---
# They call me the pipe inspector

**because I build pipelines all day**

Alright, thats it. The main pipeline is DONE AND THROUGH! It needs very little polishing, but basically... well let me tell you a little bit about it in my own words:

1. First we need someone to create a PR into main (that would be **me**, the sole **ENGINEER** of this masterpiece)
2. As soon as this hits GitHub, the autobot-merge workflow runs, and that enables auto-approve of the PR as soon as the checks pass ***(yes, I had to pay for GitHub Pro...)***
3. At the same time, the pr-validation workflow is triggered when the PR reaches github. That one performs a SAST (static code analysis - SonarQube) and image security scan (snyk). The image it produces is not saved anywhere, altough I really wanted to, but in that case it wouldn't have been possible to reach such **extreme levels of automation**. When the checks pass, the PR is auto-merged into main.
4. When that happens, the app-ci workflow is triggered (on push). It has 3 tasks: build the same image again and tag it with the digest ***(absolutely immutable practice)***, push the image to ECR, then by using the same tag, open a PR to the devopsblog-gitops repository that if accepted - changes the image reference in the dev deployment.yaml file.
5. In the gitops repo, that PR is once again enabled for auto-merge with out trustworthy autobot, and almost immidiately is auto-merged into Dev (after small secure-socket check).
6. When that happens, the pr-validation workflow is triggered and it does two different things: ZAP baseline scan (DAST gate) and if that is successful, it pushes the same changes (yes direct push) to the application deployment.yaml file.
7. And once again, of course, we run the prod-validation workflow that runs the same ZAP baseline scan again.

Done and DONE!
Took me a solid 30+ hours of work combined. Im glad that I had the free time.
Anyway, im writing this post so that I have the opportunity to check the content pipeline :D . I'll tell you how that goes next.

bing bong