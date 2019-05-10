from chatterbot.logic import LogicAdapter

class HotelsLogicAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(HotelsLogicAdapter, self).__init__(**kwargs)

    def can_process(self, statement):
        """
        Return true if the input statement contains
        'what' and 'is' and 'temperature'.
        """
        words = ['hà nội', 'hanoi', 'hà noi', 'ha nội', 'hn', 'hồ chí minh', 'hcm', 'hồ chi minh', 'ho chí minh', 'đà nẵng', 'ha noi','ho chi minh', 'da nang', "xung quanh", "khách sạn xung quanh"]
        # if all(x in statement.text.split() for x in words)
        #     return True
        # else:
        #     return False
        for word in words:
            if statement.text.lower().find(word) != -1:
                return True
        return False

    def process(self, input_statement):
        from chatterbot.conversation import Statement
        import requests

        queryCity = """
            query ($cityValue: String!) {
                hotelList(
                    hotelListCondition: {city: $cityValue}, 
                    pagerCondition: { limit: 1, pageNum: 1 }
                ) { 
                    response {
                        hotel {
                            hotelId
                            hotelName
                            hotelStarCount
                            currency
                            hotelUrl
                            hotelAmount
                            hotelSmallPicture
                            hotelZoneName
                            googleDotX
                            googleDotY
                            hotelRooms {
                                hotelRoomId
                                acreage
                                image
                                roomName
                                hotelRoomBeds {
                                    hotelRoomBedId
                                    bedType
                                    price
                                    status
                                    policies {
                                    policyId
                                    policyName
                                    icon
                                    }
                                    facilities {
                                    facilityId
                                    facilityName
                                    icon
                                    }
                                }
                            }
                        }
                        pager {
                            offset
                            limit
                            currentPageNum
                            totalCount
                            hasPrev
                            hasNext
                            prevPageNum
                            nextPageNum
                        }
                    }
                }
            }
        """
        queryNearest = """
            query {
                nearestHotelList(
                    nearestHotelListCondition: {
                        latitude: 16.0668204336316
                        longitude: 108.245087002841
                        radius: 100
                    }
                    pagerCondition: { limit: 1, pageNum: 1 }
                ) {
                    response {
                    hotel {
                        hotelId
                        hotelName
                        hotelStarCount
                        currency
                        hotelUrl
                        hotelAmount
                        hotelSmallPicture
                        hotelZoneName
                        googleDotX
                        googleDotY
                        hotelRooms {
                        hotelRoomId
                        acreage
                        image
                        roomName
                        hotelRoomBeds {
                            hotelRoomBedId
                            bedType
                            price
                            status
                            policies {
                            policyId
                            policyName
                            icon
                            }
                            facilities {
                            facilityId
                            facilityName
                            icon
                            }
                        }
                        }
                    }
                    pager {
                        offset
                        limit
                        currentPageNum
                        totalCount
                        hasPrev
                        hasNext
                        prevPageNum
                        nextPageNum
                    }
                    }
                }
            }
        """
        query = queryCity
        variables = {}
        response = {}
        api = "hotelList"
        if input_statement.text.lower().find("hà nội") != -1 or input_statement.text.lower().find("ha noi") != -1:
            query = queryCity
            variables = {
                'cityValue' : 'hà nội',
            }
            response = requests.post('http://localhost:4000/graphql', json={'query': query, 'variables': variables})
        elif input_statement.text.lower().find("hồ chí minh") != -1 or input_statement.text.lower().find("ho chi minh") != -1:
            query = queryCity
            variables = {
                'cityValue' : 'hồ chí minh',
            }
            response = requests.post('http://localhost:4000/graphql', json={'query': query, 'variables': variables})
        elif input_statement.text.lower().find("đà nẵng") != -1 or input_statement.text.lower().find("da nang") != -1:
            query = queryCity
            variables = {
                'cityValue' : 'đà nẵng',
            }
            response = requests.post('http://localhost:4000/graphql', json={'query': query, 'variables': variables})
        elif input_statement.text.lower().find("khách sạn xung quanh") != -1 or input_statement.text.lower().find("xung quanh") != -1:
            query = queryNearest
            api = "nearestHotelList"
            response = requests.post('http://localhost:4000/graphql', json={'query': query})

        # if response:
        #     return Statement('null')
        # Make a request to the temperature API
        # pager {
        #     offset
        #     limit
        #     currentPageNum
        #     totalCount
        #     hasPrev
        #     hasNext
        #     prevPageNum
        #     nextPageNum
        # }
        # print('variable: ', variables)

        data = response.json()
        hotels = data["data"][api]["response"]["hotel"]
        # Let's base the confidence value on if the request was successful
        if response.status_code == 200:
            confidence = 0.7
        else:
            confidence = 0
        
        # infor = "<div>Khách sạn: " + hotels[0]["hotelName"] + "</div>"
        # for room in hotels[0]["hotelRooms"]:
        #     infor += "<div> - Tên phòng: " + room["roomName"] + " diện tích: " + room["acreage"] + "</div>" 
        #     for roomBed in room["hotelRoomBeds"]:
        #         infor += " + Loại giường: " + roomBed["bedType"] + " có giá: " + str(roomBed["price"]) + "$" + "\n"
        for room in hotels[0]['hotelRooms']:
            infor = "<div><img src=" + room["image"] + " alt='Avatar' style='width:200px'></div>"
            infor += "<h3>" + hotels[0]["hotelName"] + "</h3>"
            infor += "<p>Diện tích: <strong>" + room["acreage"] + "</strong></p>"
            for roomBed in room["hotelRoomBeds"]:
                infor += "<p>- Giá:<strong>" + str(roomBed["price"]) + "$</strong>: " + roomBed["bedType"] + "</p>" 

        response_statement = Statement(text=infor)
        response_statement.confidence = confidence
        return response_statement