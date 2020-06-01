<div id="conversion-progress-toast" class="toast shadow" role="alert" aria-live="assertive" aria-atomic="true"
     style="position: absolute; top: 50px; right: 50px;width: 500px; background-color: darkgray">
  <div class="toast-header">
    <i data-feather="cpu"></i>
    <strong class="mr-auto">&nbsp;Converting to Python</strong>
    <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
  <div class="toast-body">
    <!-- Progress Indicator -->
    <div class="progress" style="height: 20px;">
        <div id="progress-indicator" class="progress-bar bg-success" role="progressbar" style="width: 100%;transition:none;display: block" aria-valuenow="0" aria-valuemin="100" aria-valuemax="100"></div>
    </div>
  </div>
</div>

