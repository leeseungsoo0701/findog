$(document).ready(function () {
    let map = new naver.maps.Map('map', {
        center: new naver.maps.LatLng(37.4981125, 127.0379399), // 지도의 중심 좌표
        zoom: 10, // 확대 레벨
        zoomControl: true, // 확대, 축소 아이콘 생성
        zoomControlOptions: {
            style: naver.maps.ZoomControlStyle.SMALL,
            position: naver.maps.Position.TOP_LEFT
        }
    });

    let marker =new naver.maps.Marker({
        position: new naver.maps.LatLng(37.4981125, 127.0379399), // 마커 좌표 (이후 for문으로 여러개 출력 가능)
        map: map, // 위 설정한 'map' 이름 가져오기
        icon: "{{ url_for('static', filename='rtan_heart.png') }}" // 마커 아이콘(찾습니다, 봤어요 구분)
    });
    //     naver.maps.Event.addListener(map, 'click', function(e) {
    //     marker.setPosition(e.coord);
    // });

})