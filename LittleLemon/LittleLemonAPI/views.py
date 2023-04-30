from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from .models import MenuItem, Cart, Order, OrderItem, Category
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, CustomerOrderSerializer, ManagerOrderSerializer, DeliveryCrewOrderSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User,Group
from rest_framework import status
from .permissions import IsManager
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class MenuItemsView(ListCreateAPIView):
    model = MenuItem
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    permission_classes = [IsAuthenticated]
    ordering_fields=['price']
    search_fields = ['id']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
        
    def create(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Manager').exists():
            return super().create(request, *args, **kwargs)
        else:
            return Response({'message': 'you not the manager!!'})
        

class MenuItemsRUDView(RetrieveUpdateDestroyAPIView):
    model = MenuItem
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # lookup_field = 'title'
    
    def update(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Manager').exists():
            return super().update(request, *args, **kwargs)
        else:
            return Response({'message': 'You are not in Manager group!!'})
        
    def partial_update(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Manager').exists():
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response({'message': 'You are not in Manager group!!'})
    
    def destroy(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Manager').exists():
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({'message': 'You are not in Manager group!!'})
        

class ManagerLCView(ListCreateAPIView):
    model = User
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    ordering_fields=['id']
    search_fields = ['id']
    
    
    def get_queryset(self):
        queryset = User.objects.filter(groups__name='Manager')
        return queryset
    
    def post(self, request, *args, **kwargs):
        username = self.request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Manager')
            managers.user_set.add(user)
            return Response({'message': f'User {username} was added to Manager group successfully..'}, status.HTTP_201_CREATED)
        return Response({'message': 'Error'}, status.HTTP_400_BAD_REQUEST)
        
        
class ManagerDView(DestroyAPIView):
    model = User
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        managers = user.groups.filter(name='Manager').first()
        if managers:
            managers.user_set.remove(user)
            return Response({'message': f'User {user.username} was removed from Manager group successfully..'}, status.HTTP_200_OK)
            # return super().destroy(request, *args, **kwargs)
        return Response({'message': 'User not found!!'}, status.HTTP_404_NOT_FOUND)


class DeliveryCrewLCView(ListCreateAPIView):
    model = User
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    ordering_fields=['id']
    search_fields = ['id']
    
    
    def get_queryset(self):
        queryset = User.objects.filter(groups__name='DeliveryCrew')
        return queryset
        # return super().get_queryset()
    
    def post(self, request, *args, **kwargs):
        username = self.request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='DeliveryCrew')
            managers.user_set.add(user)
            return Response({'message': f'User {username} was added to DeliveryCrew group successfully..'}, status.HTTP_201_CREATED)
        return Response({'message': 'Error'}, status.HTTP_400_BAD_REQUEST)
        # return super().post(request, *args, **kwargs)
        
        
class DeliveryCrewDView(DestroyAPIView):
    model = User
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        managers = user.groups.filter(name='DeliveryCrew').first()
        if managers:
            managers.user_set.remove(user)
            return Response({'message': f'User {user.username} was removed from DeliveryCrew group successfully..'}, status.HTTP_200_OK)
            # return super().destroy(request, *args, **kwargs)
        return Response({'message': 'User not found!!'}, status.HTTP_404_NOT_FOUND)


class CartLCView(ListCreateAPIView):
    model = Cart
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    ordering_fields=['id']
    search_fields = ['id']
    
    def get_queryset(self):
        queryset = Cart.objects.filter(user=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response({'message': 'Cart created successfully..'})

class CartDView(DestroyAPIView):
    model = Cart
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    
    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
            return Response({'message': 'Cart has been deleted successfully..'})
        else:
            return Response({'message': 'You are not authorized to delete item that does not belongs to you!!'})


class OrderLCView(ListCreateAPIView):
    model = Order
    serializer_class = CustomerOrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    ordering_fields=['id']
    search_fields = ['id']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    
    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif self.request.user.groups.filter(name='DeliveryCrew').exists():
            return Order.objects.filter(delivery_crew=self.request.user.id)
        else:
            return Order.objects.filter(user=self.request.user.id)
 
    def perform_create(self, serializer):
        user_cart = Cart.objects.filter(user=self.request.user.id)
        if user_cart:
            new_order = Order.objects.create(user=self.request.user)
            new_order.save()
            for cart_item in user_cart:
                menu_item = cart_item.menuitem
                quantity = cart_item.quantity
                unit_price = cart_item.unit_price
                order_item = OrderItem.objects.create(order=new_order, menuitem=menu_item, quantity=quantity, unit_price=unit_price)
                order_item.save()
                cart_item.delete()
            return Response({'message': 'only posting logic here'})
        else:
            return Response({'message': 'No Cart available!!'})
    def post(self, request, *args, **kwargs):
        response = self.perform_create(None)
        return response
    
    
class OrderRUDView(RetrieveUpdateDestroyAPIView):
    model = Order
    serializer_class = {
        'manager_serializer': ManagerOrderSerializer,
        'deliveryCrew_serializer': DeliveryCrewOrderSerializer,
        'customer_serializer': CustomerOrderSerializer,
    }
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    
    def get_serializer_class(self):
        if self.request.user.groups.filter(name='Manager').first():
            return self.serializer_class['manager_serializer']
        elif self.request.user.groups.filter(name='DeliveryCrew').first():
            return self.serializer_class['deliveryCrew_serializer']
        else:
            return self.serializer_class['customer_serializer']
    
    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        manager_group = self.request.user.groups.filter(name='Manager')
        deliveryCrew_group = self.request.user.groups.filter(name='DeliveryCrew')
        if order:
            serializer = self.get_serializer(order)
            if manager_group:
                return Response(serializer.data)
            elif deliveryCrew_group and order.delivery_crew.id == self.request.user.id:
                return Response(serializer.data)
            elif not manager_group and not deliveryCrew_group and order.user.id == request.user.id:
                return Response(serializer.data)
            else:
                return Response({'message': 'You are not Authorized..'})

    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').first():
            return super().destroy(request, *args, **kwargs)
        

class CategoryLCView(ListCreateAPIView):
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['id', 'title']
    search_fields = ['id', 'title']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def create(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Manager').exists():
            return super().create(request, *args, **kwargs)
        else:
            return Response({'message': 'You are not authorized!!'})
        
    
    
class CategoryRUDView(RetrieveUpdateDestroyAPIView):
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def update(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Manager').exists():
            return super().update(request, *args, **kwargs)
        else:
            return Response({'message': 'You are not in Manager group!!'})
        
    def partial_update(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Manager').exists():
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response({'message': 'You are not in Manager group!!'})
    
    def destroy(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Manager').exists():
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({'message': 'You are not in Manager group!!'})
