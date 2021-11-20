from filter import apply_grey_filter
import cProfile


pr = cProfile.Profile()
pr.enable()
apply_grey_filter('scale1200.jpg', 10, 50)
pr.disable()
pr.print_stats(sort=1)