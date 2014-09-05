<!DOCTYPE html>
<html>
<head>
    <title></title>
    <meta charset="utf-8">
    <style type="text/css">
        body{padding:10px;}
        .row{width: 100%%;min-height: 30px;}
        .divider{width: 100%%;display: block;width: 100%%;border-bottom: 2px dashed black;margin-top: 5px;margin-bottom: 5px;}
        .pull-left{display: block;float: left;}
        .pull-right{display: block;float: right;}
        .text-center{display: block;text-align: center;}
        .text-normal{font-size: 15px;}
        .text-dish{font-size: 21px; }
    </style>
</head>
<body>
<div class="text-normal">

    <div class="row">
            <div class="pull-left">小炒</div>
            <div class="pull-right">二楼包厢</div>
    </div>

    <div class="row">
        <div class="text-center">出品单</div>
    </div>

    <div class="row">
        <div class="pull-left">%s</div>
        <div class="pull-right">(%d人)</div>
    </div>

    <div class="row">
        <div class="pull-left">%s</div>
        <div class="pull-right">%s</div>
    </div>
</div>

<div class="divider"></div>

<div class="text-dish">
    <div class="row">
        %d %s %.2f
    </div>
    <div class="row">
        <div class="pull-left">(叫起)</div>

    </div>

    <div class="divider"></div>

    <div class="row">
        <div class="pull-left">%s</div>
        <div class="pull-right">%s</div>
    </div>
</div>

</body>
</html>