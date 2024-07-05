---
title: "Documentation"
no_list: true
toc_hide: true

cascade:
- type: "blog"
  toc_root: true
  _target:
    path: "/blog/**"
- type: "maestro"
  toc_root: true
  _target:
    path: "/maestro/**"
- type: "legacy"
  toc_root: true
  _target:
    path: "/legacy/**"
- type: "api_pipeline"
  toc_root: true
  _target:
    path: "/api_pipeline/**"
- type: "docs"
  _target:
    path: "/**"
---
<style>

.card {
  background-clip: border-box;
  border: 0px solid #edf2f9;
  border-radius: 0.375rem;
}

.card-footer {
  padding: 1rem 1.25rem;
  background-color: #fff;
  border-top: 0px solid #edf2f9;
}
.card-span .card-span-img {
  position: absolute;
  left: 50%;
  transform: translate3d(-50%, -50%, 0);
  width: 5rem;
  height: 5rem;
  background-color: #fff;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-span:hover, .card-span:focus {
  transform: translateY(-0.2rem);
  box-shadow: 0 1rem 4rem rgba(0, 0, 0, 0.175);
}

body {
  background-color: #edf2f9;
}

</style>

Ensuring the quality, stability and long-term maintenance of the Linux kernel
<br><br>
<div class="container">
  <div class="row row-cols-9">
    <div class="col p-3"><a href="https://www.cip-project.org/" target="_blank"><img height="64" width="64" src="/image/cip-stacked-color.svg" alt="Civil Infrastructure Platform" title="Civil Infrastructure Platform" /></a></div>
    <div class="col p-3"><a href="https://www.collabora.com/" target="_blank"><img height="64" width="64" src="/image/collabora-stacked-color.svg" alt="Collabora" title="Collabora" /></a></div>
    <div class="col p-3"><a href="https://www.google.com/" target="_blank"><img height="64" width="64" src="/image/google-color.svg" alt="Google" title="Google" /></a></div>
    <div class="col p-3"><a href="https://www.microsoft.com/" target="_blank"><img height="64" width="64" src="/image/microsoft-color.svg" alt="Microsoft" title="Microsoft" /></a></div>
    <div class="col p-3"><a href="https://www.redhat.com/" target="_blank"><img height="64" width="64" src="/image/redhat-color.svg" alt="Red Hat" title="Red Hat" /></a></div>
    <div class="col p-3"><a href="https://ti.com/" target="_blank"><img height="64" width="64" src="/image/texas-instruments.svg" alt="Texas Instruments" title="Texas Instruments" /></a></div>
    <div class="col p-3"><a href="https://www.baylibre.com/" target="_blank"><img height="64" width="64" src="/image/baylibre-horizontal-color.svg" alt="Baylibre" title="Baylibre" /></a></div>
  </div>
</div>
<br><br>
<div class="card-deck">
  <div class="card card-span">
    <div class="card-span-img">
      <i class="fas fa-bug fa-2x" align="center"></i>
    </div>
    <div class="card-body">
      <br><h3 align=center><strong>Kernel Community</strong></h3>
      <p class="card-text" align=center>The linux kernel is the focal point
of all our work.  Learn how to use CI services to help improve the code.
      </p>
    </div>
    <p class="card-footer" align=center><a href="community"><small>More information &raquo;</small></a></p>
  </div>
  <div class="card card-span">
    <div class="card-span-img">
      <i class="fas fa-flask fa-2x" align="center"></i>
    </div>
    <div class="card-body">
      <br><h3 align=center><strong>Lab Owners</strong></h3>
      <p class="card-text" align=center>Do you have hardware in a lab that you
would like to share with the community?  The linux kernel needs hardware to
test on whether it is virtual or real.  The more hardware that is available,
the more coverage that can be provided.
      </p>
    </div>
    <p class="card-footer" align=center><a href="labs"><small>More information &raquo;</small></a></p>
  </div>
  <div class="card card-span">
    <div class="card-span-img">
      <i class="fas fa-users fa-2x" align="center"></i>
    </div>
    <div class="card-body">
      <br><h3 align=center><strong>CI Service Providers</strong></h3>
      <p class="card-text" align=center>Continuous Integration only works if
we have services that expand our ecosystem to include more testing,
hardware, regression tracking, etc.  Do you have a CI service you would like
to plug in?
      </p>
    </div>
    <p class="card-footer" align=center><a href="ci-services"><small>More information &raquo;</small></a></p>
  </div>
  <div class="card card-span">
    <div class="card-span-img">
      <i class="fas fa-bullhorn fa-2x" align="center"></i>
    </div>
    <div class="card-body">
      <br><h3 align=center><strong>Contributing to KernelCI</strong></h3>
      <p class="card-text" align=center>KernelCI is an architecture that
helps build out a connected ecosystem, gathers results, and documents standards.
      </p>
    </div>
    <p class="card-footer" align=center><a href="kernelci"><small>More information &raquo;</small></a></p>
  </div>
</div>

