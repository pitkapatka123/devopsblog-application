title: I got 100 problems...
date: 2026-01-23
---
# I Got 100 Problems…

**and the IRSA is all of them**

I already told you about my precious pipelines in my last post. Everything was going well, until I decided to make yet another **GROUNDBREAKING** change.

I decided to stop burning my blog content into the images I create, but rather to store then in an s3 bucket, and have the blog app pull them from there. To avoid rebuilding my iamge every single time I post (as suggested by my mentor).

Simple?

Yeah!     ***NO!***

I managed to hit two critical problems back to back - when I build the first image using that set-up and pushed it to the dev and prod environments, all hell broke lose. First my pods failed the readiness and liveness probes. Turns out my very intelectual self forgot to set variables for the s3 bucket and s3 path (prefix), so that the application knows where to get the content from. That was an easier fix than you might think, but it still took me 1 hour to debug.

And while I was popping the champagne, happy that I fixed the error... - BAM! Internal Server Error  (500). **App was ded.**

Somewhere along the lines of logs I found this pretty little thang - ***NoCredentialsError: Unable to locate credentials***
So after another hour and a half of banging against the wall, I realized that my pods had no access to the s3 bucket. I don't know why I thought that the service accounts I created for the ALB were enough, but then I realized that a service account is namespace-scoped. And those for the ALB were in kube-system... So I wired up two new Service Accounts via ***GitOps*** ( ͡° ͜ʖ ͡°) - one for dev and one for prod, made sure that the OIDC provider IDs matched with the trusted entities and attached policies that allowed them to read the s3 bucket.

Easy fix! (he said as he was falling asleep on his desk at 02:00 am).

Anyway, we learn from our mistakes, right? Surely I gained 20 IQ after this incident. Yeah, that makes me feel better.

I'm off to get some well-deserved shuteye (while my AWS bill racks up hundreds of $).