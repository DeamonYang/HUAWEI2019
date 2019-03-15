import logging
import sys

from reader import Reader
from dispatcher import Dispatcher

logging.basicConfig(level=logging.DEBUG,
                    filename='../../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    # to read input file
    reader = Reader(car_path, cross_path, road_path)
    car_list = reader.get_cars()
    road_list = reader.get_roads()
    cross_list = reader.get_crosses()
    # for car in car_list:
    #     print(car)
    # for road in road_list:
    #     print(road)
    # for cross in cross_list:
    #     print(cross)

    # process
    dispatcher = Dispatcher(car_list, road_list, cross_list)
    result = dispatcher.run()
    for path in result:
        print(path)
    # to write output file


if __name__ == "__main__":
    main()