﻿$selectors = @(
	'Print.Fax.Scan';
	'Language.Handwriting';
	'Browser.InternetExplorer';
	'MathRecognizer';
	'OneCoreUAP.OneSync';
	'OpenSSH.Client';
	'Microsoft.Windows.MSPaint';
	'App.Support.QuickAssist';
	'Language.Speech';
	'Language.TextToSpeech';
	'App.StepsRecorder';
	'Hello.Face.18967';
	'Hello.Face.Migration.18967';
	'Hello.Face.20134';
	'Media.WindowsMediaPlayer';
	'Microsoft.Windows.WordPad';
);
$getCommand = {
  Get-WindowsCapability -Online | Where-Object -Property 'State' -NotIn -Value @(
    'NotPresent';
    'Removed';
  );
};
$filterCommand = {
  ($_.Name -split '~')[0] -eq $selector;
};
$removeCommand = {
  [CmdletBinding()]
  param(
    [Parameter( Mandatory, ValueFromPipeline )]
    $InputObject
  );
  process {
    $InputObject | Remove-WindowsCapability -Online -ErrorAction 'Continue';
  }
};
$type = 'Capability';
$logfile = 'C:\NA\Installation\RemoveCapabilities.log';
& {
	$installed = & $getCommand;
	foreach( $selector in $selectors ) {
		$result = [ordered] @{
			Selector = $selector;
		};
		$found = $installed | Where-Object -FilterScript $filterCommand;
		if( $found ) {
			$result.Output = $found | & $removeCommand;
			if( $? ) {
				$result.Message = "$type removed.";
			} else {
				$result.Message = "$type not removed.";
				$result.Error = $Error[0];
			}
		} else {
			$result.Message = "$type not installed.";
		}
		$result | ConvertTo-Json -Depth 3 -Compress;
	}
} *>&1 >> $logfile;
