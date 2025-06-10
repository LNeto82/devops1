<?php

$request_uri = $_SERVER['REQUEST_URI'];

if ($request_uri === '/payment') {
    $orderJson = file_get_contents('http://orders:3002/order');
    $orderData = json_decode($orderJson, true);

    $response = [
        'status' => 'paid',
        'order' => $orderData
    ];

    header('Content-Type: application/json');
    echo json_encode($response);
} else {
    http_response_code(404);
    echo json_encode(['error' => 'Not found']);
}
